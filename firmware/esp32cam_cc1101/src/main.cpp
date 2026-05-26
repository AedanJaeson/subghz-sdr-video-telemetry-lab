#include <Arduino.h>
#include <RadioLib.h>
#include <SPI.h>

// AI Thinker-style ESP32-CAM boards normally connect the bright white flash LED to GPIO4.
constexpr int FLASH_LED_PIN = 4;

// ESP32-CAM <-> CC1101 provisional wiring.
constexpr int CC1101_PIN_SCK = 14;
constexpr int CC1101_PIN_MISO = 12;
constexpr int CC1101_PIN_MOSI = 13;
constexpr int CC1101_PIN_CSN = 15;
constexpr int CC1101_PIN_GDO0 = 2;
constexpr int CC1101_PIN_GDO2 = 16;

// CC1101 status registers. Use the status-register read command, not normal register read.
constexpr uint8_t CC1101_REG_PARTNUM = 0x30;
constexpr uint8_t CC1101_REG_VERSION = 0x31;
constexpr uint8_t CC1101_READ_BURST = 0xC0;

constexpr unsigned long HEARTBEAT_MS = 1000;
constexpr unsigned long TX_INTERVAL_MS = 3000;

SPIClass cc1101Spi(HSPI);
Module cc1101Module(
    CC1101_PIN_CSN,
    CC1101_PIN_GDO0,
    RADIOLIB_NC,
    CC1101_PIN_GDO2,
    cc1101Spi,
    SPISettings(1000000, MSBFIRST, SPI_MODE0));
CC1101 radio(&cc1101Module);

unsigned long last_heartbeat_ms = 0;
unsigned long last_tx_ms = 0;
uint32_t heartbeat_count = 0;
uint32_t tx_count = 0;
bool led_on = false;

void blinkLed(unsigned long duration_ms) {
  digitalWrite(FLASH_LED_PIN, HIGH);
  delay(duration_ms);
  digitalWrite(FLASH_LED_PIN, LOW);
}

bool waitForMisoLow(unsigned long timeout_ms = 50) {
  const unsigned long start = millis();
  while (digitalRead(CC1101_PIN_MISO) == HIGH) {
    if (millis() - start > timeout_ms) {
      return false;
    }
    delay(1);
  }
  return true;
}

uint8_t readCc1101StatusRegister(uint8_t address, bool &ok) {
  ok = false;

  digitalWrite(CC1101_PIN_CSN, LOW);
  if (!waitForMisoLow()) {
    digitalWrite(CC1101_PIN_CSN, HIGH);
    return 0xFF;
  }

  cc1101Spi.transfer(CC1101_READ_BURST | address);
  const uint8_t value = cc1101Spi.transfer(0x00);
  digitalWrite(CC1101_PIN_CSN, HIGH);

  ok = true;
  return value;
}

void printRadioLibState(int16_t state) {
  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("success");
    return;
  }

  Serial.print("failed, RadioLib code ");
  Serial.println(state);
}

bool initializeCc1101() {
  Serial.println();
  Serial.println("CC1101 bring-up");
  Serial.println("Mode: SPI/register check first; RF TX gated by build flag.");
  Serial.print("Configured frequency MHz: ");
  Serial.println(CC1101_FREQ_MHZ, 3);
  Serial.print("Transmit enabled: ");
  Serial.println(CC1101_TRANSMIT_ENABLED ? "YES" : "NO");

  pinMode(CC1101_PIN_CSN, OUTPUT);
  digitalWrite(CC1101_PIN_CSN, HIGH);
  pinMode(CC1101_PIN_MISO, INPUT);

  cc1101Spi.begin(CC1101_PIN_SCK, CC1101_PIN_MISO, CC1101_PIN_MOSI, CC1101_PIN_CSN);
  delay(100);

  bool part_ok = false;
  bool version_ok = false;
  const uint8_t partnum = readCc1101StatusRegister(CC1101_REG_PARTNUM, part_ok);
  const uint8_t version = readCc1101StatusRegister(CC1101_REG_VERSION, version_ok);

  Serial.print("CC1101 PARTNUM read ");
  Serial.println(part_ok ? "OK" : "FAILED");
  Serial.print("CC1101 PARTNUM=0x");
  Serial.println(partnum, HEX);
  Serial.print("CC1101 VERSION read ");
  Serial.println(version_ok ? "OK" : "FAILED");
  Serial.print("CC1101 VERSION=0x");
  Serial.println(version, HEX);

  if (!part_ok || !version_ok) {
    Serial.println("CC1101 SPI FAILED - check 3V3, GND, CSN, SCK, MISO, MOSI, and module orientation.");
    return false;
  }

  ConfigFSK_t config;
  config.frequency = CC1101_FREQ_MHZ;
  config.bitRate = 4.8;
  config.frequencyDeviation = 5.0;
  config.receiverBandwidth = 125.0;
  config.power = CC1101_OUTPUT_POWER_DBM;
  config.preambleLength = 16;

  Serial.print("RadioLib CC1101 init ... ");
  const int16_t state = radio.begin(config);
  printRadioLibState(state);

  if (state != RADIOLIB_ERR_NONE) {
    Serial.println("RadioLib init failed - SPI may work but the radio configuration did not complete.");
    return false;
  }

  Serial.println("CC1101 SPI OK");
  return true;
}

void setup() {
  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);

  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("ESP32-CAM CC1101 staged bring-up");
  Serial.println("Flash LED: GPIO4");
  Serial.println("Safety: confirm local rules, legal band, verified module variant, low power, and antenna before TX.");

  blinkLed(150);
  delay(150);
  blinkLed(150);

  initializeCc1101();
}

void loop() {
  const unsigned long now = millis();

  if (now - last_heartbeat_ms >= HEARTBEAT_MS) {
    last_heartbeat_ms = now;
    led_on = !led_on;
    digitalWrite(FLASH_LED_PIN, led_on ? HIGH : LOW);

    Serial.print("heartbeat ");
    Serial.print(++heartbeat_count);
    Serial.print(" millis=");
    Serial.print(now);
    Serial.print(" led=");
    Serial.println(led_on ? "on" : "off");
  }

#if CC1101_TRANSMIT_ENABLED
  if (now - last_tx_ms >= TX_INTERVAL_MS) {
    last_tx_ms = now;
    String packet = "SUBGHZ_LAB_TEST_" + String(tx_count++);
    Serial.print("TX packet: ");
    Serial.print(packet);
    Serial.print(" ... ");
    const int16_t state = radio.transmit(packet);
    printRadioLibState(state);
  }
#else
  if (heartbeat_count % 5 == 0 && now - last_tx_ms >= 5000) {
    last_tx_ms = now;
    Serial.println("TX disabled. Set CC1101_TRANSMIT_ENABLED=1 only after RF checklist is complete.");
  }
#endif
}
