// 08 – Távolságmérés ultrahangos szenzorral, kiírás LCD-re
// A HC-SR04 egy rövid hangimpulzust küld (TRIG), majd az ECHO lábon jelzi, mennyi ideig
// tartott, amíg a visszavert hang megérkezett. Ebből számítható a távolság.

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int TRIG_PIN = 9;
const int ECHO_PIN = 8;

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Egy mérés: a visszaadott érték a távolság centiméterben.
float tavolsagMeres() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);  // 10 µs-os indítójel
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long ido = pulseIn(ECHO_PIN, HIGH);  // az ECHO impulzus hossza mikroszekundumban
  return ido * 0.0343 / 2;  // hangsebesség: 0,0343 cm/µs; oda-vissza út, ezért /2
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Tavolsag:");
}

void loop() {
  float cm = tavolsagMeres();
  lcd.setCursor(0, 1);
  lcd.print("                ");  // a 2. sor törlése (16 szóköz)
  lcd.setCursor(0, 1);
  lcd.print(cm, 0);  // egész cm-re kerekítve
  lcd.print(" cm");
  delay(500);
}
