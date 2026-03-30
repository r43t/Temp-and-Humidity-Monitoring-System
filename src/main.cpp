#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME680.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

#define SDA_PIN 21
#define SCL_PIN 22

Adafruit_BME680 bme;  // I2C mode

struct SensorSample {
  uint32_t ms;
  float temperature_c;
  float humidity_pct;
  float pressure_hpa;
  float gas_kohm;
};

QueueHandle_t sampleQueue;

void sensorTask(void *pvParameters) {
  TickType_t lastWakeTime = xTaskGetTickCount();
  const TickType_t period = pdMS_TO_TICKS(2000);

  for (;;) {
    SensorSample sample;

    if (bme.performReading()) {
      sample.ms = millis();
      sample.temperature_c = bme.temperature;
      sample.humidity_pct = bme.humidity;
      sample.pressure_hpa = bme.pressure / 100.0f;
      sample.gas_kohm = bme.gas_resistance / 1000.0f;

      // Send sample to queue. If queue is full, this sample is dropped.
      xQueueSend(sampleQueue, &sample, 0);
    }

    // Keep this task on a fixed 2-second cadence
    xTaskDelayUntil(&lastWakeTime, period);
  }
}

void serialTask(void *pvParameters) {
  SensorSample sample;

  // CSV header so the PC script can ignore or parse it
  Serial.println("ms,temp_c,humidity_pct,pressure_hpa,gas_kohm");

  for (;;) {
    if (xQueueReceive(sampleQueue, &sample, portMAX_DELAY) == pdTRUE) {
      Serial.print(sample.ms);
      Serial.print(",");
      Serial.print(sample.temperature_c, 2);
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
  Serial.begin(115200);
  delay(1000);

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!bme.begin(0x77)) {
    Serial.println("ERROR: BME680 not found at 0x77");
    while (true) {
      delay(1000);
    }
  }

  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  sampleQueue = xQueueCreate(10, sizeof(SensorSample));
  if (sampleQueue == NULL) {
    Serial.println("ERROR: Failed to create queue");
    while (true) {
      delay(1000);
    }
  }

  // Pin both app tasks to Core 1 for simplicity
  xTaskCreatePinnedToCore(
    sensorTask,
    "SensorTask",
    4096,
    NULL,
    1,
    NULL,
    1
  );

  xTaskCreatePinnedToCore(
    serialTask,
    "SerialTask",
    4096,
    NULL,
    1,
    NULL,
    1
  );
}

void loop() {
  // Nothing application-critical happens here
  vTaskDelay(pdMS_TO_TICKS(1000));
}