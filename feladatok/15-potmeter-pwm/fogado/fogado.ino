// 15 – Potméter és PWM, fogadó Arduino (bal oldali)
// A küldőtől érkező potméterértéket (0–1023) átszámolja PWM-kitöltésre (0–255),
// és ezzel állítja a 9-es lábra kötött LED fényerejét.
// A küldő Arduino a kuldo/kuldo.ino programot futtatja.

const int LED_PIN = 9;  // PWM-képes láb (az Unón ~ jelöli)

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String sor = Serial.readStringUntil('\n');
    int ertek = sor.toInt();                     // 0–1023
    int fenyero = map(ertek, 0, 1023, 0, 255);  // 0–255
    analogWrite(LED_PIN, fenyero);
    Serial.print("Fényerő: ");
    Serial.println(fenyero);
  }
}
