// 01 – A beépített LED villogtatása
// Az Arduino Uno 13-as lábára gyárilag egy LED van kötve (LED_BUILTIN).

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);  // a LED lábát kimenetnek állítjuk
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // LED be
  delay(1000);                      // 1 másodperc várakozás
  digitalWrite(LED_BUILTIN, LOW);   // LED ki
  delay(1000);
}
