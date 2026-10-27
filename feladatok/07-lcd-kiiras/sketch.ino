// 07 – Szöveg kiírása I2C-s 16x2-es LCD kijelzőre
// Az első sorban állandó szöveg, a másodikban az indítás óta eltelt másodpercek.
// Az LCD ékezetes betűket nem tud megjeleníteni, ezért a szövegek ékezet nélküliek.

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C-cím, oszlopok, sorok

void setup() {
  lcd.init();       // a kijelző indítása
  lcd.backlight();  // háttérvilágítás be
  lcd.setCursor(0, 0);  // 1. oszlop, 1. sor (a számozás 0-tól indul)
  lcd.print("Hello, Robotika!");
}

void loop() {
  lcd.setCursor(0, 1);  // 1. oszlop, 2. sor
  lcd.print("Eltelt: ");
  lcd.print(millis() / 1000);
  lcd.print(" s");
  delay(1000);
}
