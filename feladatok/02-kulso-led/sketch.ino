// 02 – Külső LED villogtatása
// A LED a 8-as lábra van kötve egy 220 Ω-os előtétellenálláson keresztül.

const int LED_PIN = 8;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
