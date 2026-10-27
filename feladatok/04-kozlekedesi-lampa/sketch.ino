// 04 – Közlekedési lámpa
// Ciklus: piros (3 s) → piros + sárga (1 s) → zöld (3 s) → sárga (1 s) → újra piros.

const int PIROS_PIN = 10;
const int SARGA_PIN = 9;
const int ZOLD_PIN = 8;

// Egyszerre beállítja mindhárom LED állapotát.
void lampa(int piros, int sarga, int zold) {
  digitalWrite(PIROS_PIN, piros);
  digitalWrite(SARGA_PIN, sarga);
  digitalWrite(ZOLD_PIN, zold);
}

void setup() {
  pinMode(PIROS_PIN, OUTPUT);
  pinMode(SARGA_PIN, OUTPUT);
  pinMode(ZOLD_PIN, OUTPUT);
}

void loop() {
  lampa(HIGH, LOW, LOW);   // piros
  delay(3000);
  lampa(HIGH, HIGH, LOW);  // piros + sárga
  delay(1000);
  lampa(LOW, LOW, HIGH);   // zöld
  delay(3000);
  lampa(LOW, HIGH, LOW);   // sárga
  delay(1000);
}
