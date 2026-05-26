#include <Arduino.h>

// AI Thinker-style ESP32-CAM boards normally connect the bright white flash LED
// to GPIO4. This sketch is only a programming/power/serial smoke test.
constexpr int FLASH_LED_PIN = 4;
constexpr unsigned long BLINK_MS = 500;

unsigned long last_toggle_ms = 0;
bool led_on = false;
unsigned long boot_count = 0;

void setup() {
  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);

  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("ESP32-CAM HW-409 smoke test");
  Serial.println("Flash LED: GPIO4");
  Serial.println("Expected: LED blinks and serial heartbeat prints every 500 ms.");
}

void loop() {
  const unsigned long now = millis();
  if (now - last_toggle_ms >= BLINK_MS) {
    last_toggle_ms = now;
    led_on = !led_on;
    digitalWrite(FLASH_LED_PIN, led_on ? HIGH : LOW);

    Serial.print("heartbeat ");
    Serial.print(++boot_count);
    Serial.print(" millis=");
    Serial.print(now);
    Serial.print(" led=");
    Serial.println(led_on ? "on" : "off");
  }
}
