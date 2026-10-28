// 15 – Potméter és PWM, küldő Arduino (jobb oldali)
// Az A0 lábra kötött potméter állását (0–1023) tizedmásodpercenként elküldi a fogadónak.
// A fogadó Arduino a fogado/fogado.ino programot futtatja.

const int POT_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int ertek = analogRead(POT_PIN);  // 0 V -> 0, 5 V -> 1023
  Serial.println(ertek);
  delay(100);
}
