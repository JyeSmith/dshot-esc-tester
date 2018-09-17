#define DEMCR_TRCENA    0x01000000
#define DEMCR (*((volatile uint32_t *)0xE000EDFC))
#define DWT_CTRL (*(volatile uint32_t *)0xe0001000)
#define CYCCNTENA (1<<0)
#define DWT_CYCCNT ((volatile uint32_t *)0xE0001004)
#define CPU_CYCLES *DWT_CYCCNT

void setup() {

    // dshot output pin
    pinMode(PC13, OUTPUT);
    // potentiometer input pin
    pinMode(PA0, INPUT_ANALOG);
      
    // setup for delayNanosecond()
    DEMCR |= DEMCR_TRCENA;
    *DWT_CYCCNT = 0;
    DWT_CTRL |= CYCCNTENA;

    // output disarm signal while esc initialises
    uint16_t currentTime = millis();
    while (millis() < currentTime + 5000) {
        dshotOutput(0); 
        delay(1);
    }
}
void loop() {

    uint16_t potentiometerReading = 0;
    for (uint8_t i = 0; i < 15; i++) {
      potentiometerReading += analogRead(PA0);
    }
    potentiometerReading /= 15;
    
    dshotOutput(
      map(potentiometerReading, 0, 4095, 48, 2047)
      ); 
      
    delay(1);

}

uint16_t dshotOutput(uint16_t throttle) {

    // telemetry bit
    uint16_t packet = (throttle << 1) | 0;

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

    uint16_t returnPacket = packet;

    // delays are for dshot150
    for (int i = 0; i < 16; i++) {
        gpio_write_bit(GPIOC, 13, HIGH);
        delayNanoseconds(2500);
        if (packet & 0x8000) {
            delayNanoseconds(2500);
            gpio_write_bit(GPIOC, 13, LOW);
        } else {
            gpio_write_bit(GPIOC, 13, LOW);
            delayNanoseconds(2500);
        }
        delayNanoseconds(1667);
        packet <<= 1;
    }

    return returnPacket;
}

void delayNanoseconds(uint16_t delayTime) {
    
    uint32_t endCycles = CPU_CYCLES + (delayTime / 72); // 72 MHz
    
    while (CPU_CYCLES < endCycles) {
    }

    return;
}






