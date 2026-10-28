// 10 – Nyomógomb: amíg le van nyomva, világít a beépített LED
// A gomb a 2-es láb és a GND közé van kötve. A belső felhúzó ellenállás (INPUT_PULLUP)
// miatt a láb alapállapotban HIGH, lenyomott gombnál LOW.

const int GOMB_PIN = 2;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(GOMB_PIN, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(GOMB_PIN) == LOW) {  // le van nyomva
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
