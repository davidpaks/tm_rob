// 14 – Soros kommunikáció, fogadó Arduino (bal oldali)
// A küldőtől érkező számot (RX, 0-s láb) beolvassa, és kiírja a soros monitorra.
// A küldő Arduino a kuldo/kuldo.ino programot futtatja.

void setup() {
  Serial.begin(9600);  // ugyanaz az átviteli sebesség, mint a küldőn
}

void loop() {
  if (Serial.available() > 0) {                // érkezett-e adat?
    String sor = Serial.readStringUntil('\n');  // beolvasás a sor végéig
    int szam = sor.toInt();                     // szövegből szám
    Serial.print("Kapott szám: ");
    Serial.println(szam);
  }
}
