// 03 – Két LED villogtatása felváltva
// Mindig csak az egyik LED világít, 1 másodpercenként cserélnek.

const int LED1_PIN = 8;
const int LED2_PIN = 9;

void setup() {
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED1_PIN, HIGH);
  digitalWrite(LED2_PIN, LOW);
  delay(1000);
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, HIGH);
  delay(1000);
}
