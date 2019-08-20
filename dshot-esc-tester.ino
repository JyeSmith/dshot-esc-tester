/*
 * ----------------------------------------------------------------------------
 * "THE PROP-WARE LICENSE" (Revision 42):
 * <https://github.com/JyeSmith> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me some props in return.   Jye Smith
 * ----------------------------------------------------------------------------
 */

/* Some of the below code is taken from examples provided by Felix on RCGroups.com
 * 
 * KISS ESC 24A Serial Example Code for Arduino.
 * https://www.rcgroups.com/forums/showthread.php?2555162-KISS-ESC-24A-Race-Edition-Flyduino-32bit-ESC
 * https://www.rcgroups.com/forums/showatt.php?attachmentid=8521072&d=1450345654 * 
 */

#include <HardwareSerial.h>
#include "SSD1306.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "Arduino.h"
#include "esp32-hal.h"
#include "HX711.h"

#define MOTOR_POLES 14

// HX711
#define LOADCELL_DOUT_PIN     25
#define LOADCELL_SCK_PIN      26
#define LOADCELL_CALIBRATION  200.0
HX711 loadcell;

TaskHandle_t Task1;

rmt_data_t dshotPacket[16];
rmt_obj_t* rmt_send = NULL;

hw_timer_t * timer = NULL;

HardwareSerial MySerial(1);

SSD1306  display(0x3c, 21, 22);  // 21 and 22 are default pins

uint8_t receivedBytes = 0;
volatile bool requestTelemetry = false;
uint16_t dshotUserInputValue = 0;
int16_t ESC_telemetrie[5]; // Temperature, Voltage, Current, used mAh, eRpM

uint8_t temperature = 0;
uint8_t temperatureMax = 0;
float voltage = 0;
float voltageMin = 99;
uint32_t current = 0;
uint32_t currentMax = 0;
uint32_t erpm = 0;
uint32_t erpmMax = 0;
uint32_t rpm = 0;
uint32_t rpmMAX = 0;
uint32_t kv = 0;
uint32_t kvMax = 0;

void gotTouch8(){
    dshotUserInputValue = 0;
    } // DIGITAL_CMD_MOTOR_STOP
void gotTouch9(){
    dshotUserInputValue = 247;
    resetMaxMinValues();
    } // 10%
void gotTouch7(){
    dshotUserInputValue = 447;
    resetMaxMinValues();
    } // 20%
void gotTouch6(){
    dshotUserInputValue = 1047;
    resetMaxMinValues();
    } // 50%
void gotTouch5(){ 
    dshotUserInputValue = 2047;                 
    resetMaxMinValues();
    } // 100%
void gotTouch4(){ 
    temperatureMax = 0;
    voltageMin = 99;
    currentMax = 0;
    erpmMax = 0;
    rpmMAX = 0;
    kvMax = 0;
}
void resetMaxMinValues() {
    gotTouch4();
}

void IRAM_ATTR getTelemetry(){
    requestTelemetry = true;        
}

void startTelemetryTimer() {
    timer = timerBegin(0, 80, true); // timer_id = 0; divider=80; countUp = true;
    timerAttachInterrupt(timer, &getTelemetry, true); // edge = true
    timerAlarmWrite(timer, 20000, true);  //1000 = 1 ms
    timerAlarmEnable(timer);
}

// Second core used to handle dshot packets
void secondCoreTask( void * pvParameters ){
    while(1){
      
        dshotOutput(dshotUserInputValue, requestTelemetry);
    
        if (requestTelemetry) {                
            requestTelemetry = false;
            receivedBytes = 0;
        }
        
        delay(1);
        
    } 
}

void setup() {

    Serial.begin(115200);
    MySerial.begin(115200, SERIAL_8N1, 16, 17);

    loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    loadcell.set_scale(LOADCELL_CALIBRATION);
    loadcell.tare();  
    
    if ((rmt_send = rmtInit(5, true, RMT_MEM_64)) == NULL) {
        Serial.println("init sender failed\n");
    }

    float realTick = rmtSetTick(rmt_send, 12.5); // 12.5ns sample rate
    Serial.printf("rmt_send tick set to: %fns\n", realTick);
  
    display.init();
    display.flipScreenVertically();
    display.setFont(ArialMT_Plain_10); 
    
    // Output disarm signal while esc initialises and do some display stuff.
    uint8_t xbeep = random(15, 100);
    uint8_t ybeep = random(15, 50);
    uint8_t ibeep = 0;
    while (millis() < 3500) {
        dshotOutput(0, false);
        delay(1);  
        
        display.clear();            
        ibeep++; 
        if (ibeep == 100) {
            ibeep = 0;
            xbeep = random(15, 50);
            ybeep = random(15, 50);
        }
        display.drawString(xbeep, ybeep, "beep");
        if (millis() < 500) {         
            display.drawString(0, 0, "Initialising ESC... 4s");
        } else if (millis() < 1500) {   
            display.drawString(0, 0, "Initialising ESC... 3s");
        } else if (millis() < 2500) {  
            display.drawString(0, 0, "Initialising ESC... 2s");
        } else {                
            display.drawString(0, 0, "Initialising ESC... 1s");
        }
        display.display(); 
    }
    
    touchAttachInterrupt(T4, gotTouch4, 40);
    touchAttachInterrupt(T5, gotTouch5, 40);
    touchAttachInterrupt(T6, gotTouch6, 40);
    touchAttachInterrupt(T7, gotTouch7, 40);
    touchAttachInterrupt(T8, gotTouch8, 40);
    touchAttachInterrupt(T9, gotTouch9, 40);

    // Empty Rx Serial of garbage telemtry
    while(MySerial.available())
        MySerial.read();
    
    requestTelemetry = true;
    
    BeginWebUpdate();

    startTelemetryTimer(); // Timer used to request tlm continually in case ESC rcv bad packet
    
    xTaskCreatePinnedToCore(secondCoreTask, "Task1", 10000, NULL, 1, &Task1, 0); 

}

void loop() {

    HandleWebUpdate();

    if(!requestTelemetry) {
         receiveTelemtrie();
    }

}

void receiveTelemtrie(){
    static uint8_t SerialBuf[10];

        if(MySerial.available()){
            SerialBuf[receivedBytes] = MySerial.read();
            receivedBytes++;
        }

        if(receivedBytes > 9){ // transmission complete
          
            uint8_t crc8 = get_crc8(SerialBuf, 9); // get the 8 bit CRC
          
            if(crc8 != SerialBuf[9]) {
                Serial.println("CRC transmission failure");
                
                // Empty Rx Serial of garbage telemtry
                while(MySerial.available())
                    MySerial.read();
                
                requestTelemetry = true;
            
                return; // transmission failure 
            }
          
            // compute the received values
            ESC_telemetrie[0] = SerialBuf[0]; // temperature
            ESC_telemetrie[1] = (SerialBuf[1]<<8)|SerialBuf[2]; // voltage
            ESC_telemetrie[2] = (SerialBuf[3]<<8)|SerialBuf[4]; // Current
            ESC_telemetrie[3] = (SerialBuf[5]<<8)|SerialBuf[6]; // used mA/h
            ESC_telemetrie[4] = (SerialBuf[7]<<8)|SerialBuf[8]; // eRpM *100
                  
    //      Serial.println("Requested Telemetrie");
    //      Serial.print("Temperature (C): ");
    //      Serial.println(ESC_telemetrie[0]); 
    //      Serial.print("Voltage (V): ");
    //      Serial.println(ESC_telemetrie[1] / 100.0);   
    //      Serial.print("Current (mA): ");
    //      Serial.println(ESC_telemetrie[2] * 100); 
    //      Serial.print("mA/h: ");
    //      Serial.println(ESC_telemetrie[3] * 10);   
    //      Serial.print("eRPM : ");
    //      Serial.println(ESC_telemetrie[4] * 100);  
    //      Serial.print("RPM : ");
    //      Serial.println(ESC_telemetrie[4] * 100 / 7.0);  // 7 = 14 magnet count / 2
    //      Serial.print("KV : ");
    //      Serial.println( (ESC_telemetrie[4] * 100 / 7.0) / (ESC_telemetrie[1] / 100.0) );  // 7 = 14 magnet count / 2
    //      Serial.println(" ");
    //      Serial.println(" ");


          Serial.print(millis()); 
          Serial.print(","); 
    //      Serial.print("Temperature (C): ");
          Serial.print(ESC_telemetrie[0]); 
          Serial.print(","); 
    //      Serial.print("Voltage (V): ");
          Serial.print(ESC_telemetrie[1] / 100.0); 
          Serial.print(",");   
    //      Serial.print("Current (mA): ");
          Serial.print(ESC_telemetrie[2] * 100); 
          Serial.print(","); 
    //      Serial.print("mA/h: ");
          Serial.print(ESC_telemetrie[3] * 10);  
          Serial.print(",");  
    //      Serial.print("eRPM : ");
          Serial.print(ESC_telemetrie[4] * 100); 
          Serial.print(",");  
          
          if (loadcell.is_ready()) {
              long reading = loadcell.get_units(1);
              Serial.println(reading);
          } else {
              Serial.println();
          }

          
            temperature = 0.9*temperature + 0.1*ESC_telemetrie[0];
            if (temperature > temperatureMax) {
                temperatureMax = temperature;
            }
            
            voltage = 0.9*voltage + 0.1*(ESC_telemetrie[1] / 100.0);
            if (voltage < voltageMin) {
                voltageMin = voltage;
            }
            
            current = 0.9*current + 0.1*(ESC_telemetrie[2] * 100);
            if (current > currentMax) {
                currentMax = current;
            }
            
            erpm = 0.9*erpm + 0.1*(ESC_telemetrie[4] * 100);
            if (erpm > erpmMax) {
                erpmMax = erpm;
            }
            
            rpm = erpm / (MOTOR_POLES / 2);
            if (rpm > rpmMAX) {
                rpmMAX = rpm;
            }
            
            if (rpm) {                  // Stops weird numbers :|
                kv = rpm / voltage;
            } else {
                kv = 0;
            }
            if (kv > kvMax) {
                kvMax = kv;
            }

            updateDisplay();
            requestTelemetry = true;
          
        }

  return;
  
}

void dshotOutput(uint16_t value, bool telemetry) {
    
    uint16_t packet;
    
    // telemetry bit    
    if (telemetry) {
        packet = (value << 1) | 1;
    } else {
        packet = (value << 1) | 0;
    }

    // https://github.com/betaflight/betaflight/blob/09b52975fbd8f6fcccb22228745d1548b8c3daab/src/main/drivers/pwm_output.c#L523
    int csum = 0;
    int csum_data = packet;
    for (int i = 0; i < 3; i++) {
        csum ^=  csum_data;
        csum_data >>= 4;
    }
    csum &= 0xf;
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
    
    return;

}

uint8_t update_crc8(uint8_t crc, uint8_t crc_seed){
  uint8_t crc_u, i;
  crc_u = crc;
  crc_u ^= crc_seed;
  for ( i=0; i<8; i++) crc_u = ( crc_u & 0x80 ) ? 0x7 ^ ( crc_u << 1 ) : ( crc_u << 1 );
  return (crc_u);
}

uint8_t get_crc8(uint8_t *Buf, uint8_t BufLen){
  uint8_t crc = 0, i;
  for( i=0; i<BufLen; i++) crc = update_crc8(Buf[i], crc);
  return (crc);
}

void updateDisplay() {    
    display.clear();
              
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.drawString(0,  0, "Dshot Packet");
    display.drawString(0, 10, "Temp C");
    display.drawString(0, 20, "Volt");
    display.drawString(0, 30, "mA");
    display.drawString(0, 40, "eRPM");
    display.drawString(0, 50, "KV");
    
    display.setTextAlignment(TEXT_ALIGN_RIGHT);
    display.drawString(80, 10, String(temperature));
    display.drawString(80, 20, String(voltage));
    display.drawString(80, 30, String(current));
    display.drawString(80, 40, String(erpm));
    display.drawString(80, 50, String(kv));
    
    display.setTextAlignment(TEXT_ALIGN_RIGHT);
    display.drawString(128,  0, String(dshotUserInputValue));
    display.drawString(128, 10, String(temperatureMax));
    display.drawString(128, 20, String(voltageMin));
    display.drawString(128, 30, String(currentMax));
    display.drawString(128, 40, String(erpmMax));
    display.drawString(128, 50, String(kvMax));
    
    display.display();  
}
