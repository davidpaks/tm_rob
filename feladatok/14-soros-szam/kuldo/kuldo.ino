// 14 – Soros kommunikáció, küldő Arduino (jobb oldali)
// Másodpercenként elküld egy számot a soros vonalon (TX, 1-es láb), minden alkalommal eggyel nagyobbat.
// A fogadó Arduino a fogado/fogado.ino programot futtatja.

int szam = 0;

void setup() {
  Serial.begin(9600);  // átviteli sebesség: a fogadón is ugyanennyi legyen
}

void loop() {
  Serial.println(szam);  // a szám szövegként, sorvége jellel lezárva megy el
  szam++;
  delay(1000);
}
