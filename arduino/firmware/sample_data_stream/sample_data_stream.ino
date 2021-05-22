#include <CAN.h>

void setup() {
    // using a high baud for testing purposes
    Serial.begin(2000000);
}

void loop() {
    Serial.println("0x1B4,2E,D4,E0,F3,00,30,FC,BA");
    delay(1);
}
