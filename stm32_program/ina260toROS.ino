#include <Adafruit_INA260.h>

Adafruit_INA260 ina260 = Adafruit_INA260();

void setup() {
  int SDA = 19;
  int SCL = 21;
  Wire.begin(SDA, SCL);
  
  Serial.begin(115200);
  // Wait until serial port is opened
  while (!Serial) { delay(10); }

  Serial.println("Adafruit INA260 Test");

  if (!ina260.begin()) {
    Serial.println("Couldn't find INA260 chip");
    while (1);
  }
  Serial.println("Found INA260 chip");
}

void loop() {
  long current = long(ina260.readCurrent() * 1000);
  long voltage = long(ina260.readBusVoltage() * 1000);

  char char_temp[4] = {0};
  *(long *)char_temp = current;
  Serial.print("i");
  for(int i=0; i<=3; i++)
  {
    Serial.print(char_temp[i]);
  }
  Serial.print("\n");
  
  *(long *)char_temp = voltage;
  Serial.print("v");
  for(int i=0; i<=3; i++)
  {
    Serial.print(char_temp[i]);
  }
  Serial.print("\n");

  delay(100);
}