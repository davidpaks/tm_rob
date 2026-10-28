// 12 – Két nyomógomb: az egyik felkapcsolja, a másik lekapcsolja a beépített LED-et
// Mindkét gomb INPUT_PULLUP módban van, lenyomva LOW.

const int BE_PIN = 2;  // zöld gomb: felkapcsol
const int KI_PIN = 3;  // piros gomb: lekapcsol

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(BE_PIN, INPUT_PULLUP);
  pinMode(KI_PIN, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(BE_PIN) == LOW) {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  if (digitalRead(KI_PIN) == LOW) {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
