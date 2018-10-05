#define DSHOT_COMMAND_DELAY_MS 1

void setup() {

    // dshot output pin
    pinMode(PC13, OUTPUT);
    // potentiometer input pin
    pinMode(PA0, INPUT_ANALOG);

    // output disarm signal while esc initialises
    uint16_t currentTime = millis();
    while (millis() < currentTime + 5000) {
        dshotOutput(0);
    }

}

void loop() {

    dshotOutput(
      map(analogRead(PA0), 0, 4095, 48, 2047)
      );

}

void dshotOutput(uint16_t throttle) {

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

    // delays are for ~dshot300
    for (int i = 0; i < 16; i++) {
        if (packet & 0x8000) {
            gpio_write_bit(GPIOC, 13, HIGH);
            delayMicroseconds(2);
            gpio_write_bit(GPIOC, 13, LOW);
            delayMicroseconds(1);
        } else {
            gpio_write_bit(GPIOC, 13, HIGH);
            delayMicroseconds(1);
            gpio_write_bit(GPIOC, 13, LOW);
            delayMicroseconds(2);
        }
        packet <<= 1;
    }

    delay(DSHOT_COMMAND_DELAY_MS); // delay required between dshot packets
    
    return;

}
