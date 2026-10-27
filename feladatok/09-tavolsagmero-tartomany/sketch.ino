// 09 – Távolságmérés a mérési tartomány figyelésével
// A HC-SR04 kb. 2 cm és 4 m között mér megbízhatóan. Ha a mért érték ezen kívül esik,
// a kijelző ezt jelzi. 1 m alatt centiméterben, felette méterben írja ki a távolságot.

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int TRIG_PIN = 9;
const int ECHO_PIN = 8;
const float MIN_CM = 2;
const float MAX_CM = 400;

LiquidCrystal_I2C lcd(0x27, 16, 2);

float tavolsagMeres() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long ido = pulseIn(ECHO_PIN, HIGH, 30000);  // legfeljebb 30 ms-ig vár (kb. 5 m)
  return ido * 0.0343 / 2;  // ha nem jött visszhang, az ido 0, így a távolság is 0
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
  if (cm < MIN_CM || cm > MAX_CM) {
    lcd.print("Kivul: 2cm-4m");
  } else if (cm < 100) {
    lcd.print(cm, 0);
    lcd.print(" cm");
  } else {
    lcd.print(cm / 100, 2);  // méterben, két tizedesjeggyel
    lcd.print(" m");
  }
  delay(500);
}
