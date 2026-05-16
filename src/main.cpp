#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME680.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

#define SDA_PIN 21  // GPIO 21 for I2C data pin
#define SCL_PIN 22  // GPIO 22 for I2C clock pin

Adafruit_BME680 bme;  // BME680 sensor object set to I2C mode

struct SensorSample {   // structure to hold one complete sensor reading
  uint32_t ms;          // timestamp in milliseconds
  float temperature_c;
  float humidity_pct;
  float pressure_hpa;
  float gas_kohm;
};
QueueHandle_t sampleQueue;        // FreeRTOS queue for passing sensor data between tasks

// task 1 reads sensor data every 2 seconds and pushes it to the queue
void sensorTask(void *pvParameters) {
  TickType_t lastWakeTime = xTaskGetTickCount();    // reference time
  const TickType_t period = pdMS_TO_TICKS(2000);    // 2 second period

  while (true) {
    SensorSample sample;        // structure to hold current reading
    
    if (bme.performReading()) { // read sensor data (returns false if read fails)
      sample.ms = millis();     // get timestamp
      sample.temperature_c = bme.temperature;
      sample.humidity_pct = bme.humidity;
      sample.pressure_hpa = bme.pressure / 100.0f;    // converting Pa to hPa
      sample.gas_kohm = bme.gas_resistance / 1000.0f; // converting ohm to kiloohm
      xQueueSend(sampleQueue, &sample, 0);  // send sample to queue, If queue is full, sample gets dropped
    }
    xTaskDelayUntil(&lastWakeTime, period); // delay until next period
  }
}
// task 2 waits for data from queue and prints it over serial (UART)
void serialTask(void *pvParameters) {
  SensorSample sample;

  while(true) {
    // wait until new sample is available
    if (xQueueReceive(sampleQueue, &sample, portMAX_DELAY) == pdTRUE) {
      // separated by commas for easy parsing
      Serial.print(sample.ms);
      Serial.print(",");
      Serial.print(sample.temperature_c, 2);  // prints values to 2 decimal places
      Serial.print(",");
      Serial.print(sample.humidity_pct, 2);
      Serial.print(",");
      Serial.print(sample.pressure_hpa, 2);
      Serial.print(",");
      Serial.println(sample.gas_kohm, 2);
    }
  }
}

void setup() {
  Serial.begin(115200);   // serial comm start
  delay(1000);            // delay for serial monitor to connect

  Wire.begin(SDA_PIN, SCL_PIN);   // initialize I2C

  if (!bme.begin(0x77)) { // BME sensor I2C address is 0x77
    Serial.println("ERROR: BME680 not found at 0x77");
    while (true) {
      delay(1000);
    }
  }
  // configuring the sensor settings
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);
  
  // queue can handle up to 10 samples
  sampleQueue = xQueueCreate(10, sizeof(SensorSample));
  if (sampleQueue == NULL) {
    Serial.println("ERROR: Failed to create queue");  // stop if fail
    while (true) {
      delay(1000);
    }
  }
  // Pin both tasks to ESP32 Core 1 for predictable timing (stability), 4 KB stack memory for each 
  xTaskCreatePinnedToCore(sensorTask, "SensorTask", 4096, NULL, 2, NULL, 1);  // priority 2 task
  xTaskCreatePinnedToCore(serialTask, "SerialTask", 4096, NULL, 1, NULL, 1);  // priority 1 task
}

void loop() {
  // run task, sleep for 1 second and repeat (reduces CPU load and jitter)
  vTaskDelay(pdMS_TO_TICKS(1000));
}