
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "Arduino.h"
#include "esp32-hal.h"

#define POTENTIOMETER_PIN 4

rmt_data_t dshotPacket[16];
rmt_data_t dshotTelemetry[16];

rmt_obj_t* rmt_send = NULL;

void setup() {

    Serial.begin(115200);
    
    // potentiometer input pin
    pinMode(POTENTIOMETER_PIN, INPUT);

    if ((rmt_send = rmtInit(12, true, RMT_MEM_64)) == NULL) {
        Serial.println("init sender failed\n");
    }

    float realTick = rmtSetTick(rmt_send, 12.5); // 12.5ns sample rate
    Serial.printf("real tick set to: %fns\n", realTick);
    
    // output disarm signal while esc initialises
    uint16_t currentTime = millis();
    while (millis() < currentTime + 2000) {
        dshotOutput(0, false);
    }

    // 33 DIGITAL_CMD_SIGNAL_LINE_TELEMETRY_ENABLE  // Need 6x, no wait required. Enables commands 42 to 47
    for (int i = 0; i < 6; i++) {
        dshotOutput(33, false); 
    }
    
}

void loop() {

    int potentiometer = analogRead(POTENTIOMETER_PIN);
    
    if (potentiometer < 50) {
        dshotOutput(0, false);
    } else {
        dshotOutput(
          map(potentiometer, 0, 4095, 48, 2047),
          false
        );
    }
//    dshotOutput(300, false); // test output with no potentiometer

//42 DIGITAL_CMD_SIGNAL_LINE_TEMPERATURE_TELEMETRY      // No wait required 
//43 DIGITAL_CMD_SIGNAL_LINE_VOLTAGE_TELEMETRY          // No wait required 
//44 DIGITAL_CMD_SIGNAL_LINE_CURRENT_TELEMETRY          // No wait required 
//45 DIGITAL_CMD_SIGNAL_LINE_CONSUMPTION_TELEMETRY      // No wait required 
//46 DIGITAL_CMD_SIGNAL_LINE_ERPM_TELEMETRY             // No wait required 
//47 DIGITAL_CMD_SIGNAL_LINE_ERPM_PERIOD_TELEMETRY      // No wait required 

//    dshotOutput(42, true);
         
}

void dshotOutput(uint16_t value, bool telemetry) {

    uint16_t packet;
    
    // telemetry bit    
    if (telemetry) {
        packet = (value << 1) | 1;
    } else {
        packet = (value << 1) | 0;
    }

    // compute checksum
    // https://github.com/betaflight/betaflight/blob/09b52975fbd8f6fcccb22228745d1548b8c3daab/src/main/drivers/pwm_output.c#L523
    int csum = 0;
    int csum_data = packet;
    for (int i = 0; i < 3; i++) {
        csum ^=  csum_data;   // xor data by nibbles
        csum_data >>= 4;
    }
    csum &= 0xf;
    // append checksum
    packet = (packet << 4) | csum;

    // durations are for dshot600
    // https://blck.mn/2016/11/dshot-the-new-kid-on-the-block/
    // Bit length (total timing period) is 1.67 microseconds (T0H + T0L or T1H + T1L).
    // For a bit to be 1, the pulse width is 1250 nanoseconds (T1H – time the pulse is high for a bit value of ONE)
    // For a bit to be 0, the pulse width is 625 nanoseconds (T0H – time the pulse is high for a bit value of ZERO)
    for (int i = 0; i < 16; i++) {
        if (packet & 0x8000) {
              dshotPacket[i].level0 = 1;
              dshotPacket[i].duration0 = 100;
              dshotPacket[i].level1 = 0;
              dshotPacket[i].duration1 = 34;
          } else {
              dshotPacket[i].level0 = 1;
              dshotPacket[i].duration0 = 50;
              dshotPacket[i].level1 = 0;
              dshotPacket[i].duration1 = 84;
          }
        packet <<= 1;
    }
    
    rmtWrite(rmt_send, dshotPacket, 16);
    
    delayMicroseconds(250);  // delay for ~4kHz loop
        
    return;

}
