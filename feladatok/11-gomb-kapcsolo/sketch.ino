// 11 – Nyomógomb kapcsolóként: minden lenyomás átváltja a LED állapotát
// Nem az számít, hogy a gomb le van-e nyomva, hanem a lenyomás pillanata.
// Pergésmentesítés millis()-szel: a gomb állapotát csak akkor fogadjuk el, ha már
// 50 ms óta nem változott. Közben a loop() nem áll meg, tehát mást is csinálhatna.

const int GOMB_PIN = 2;
const unsigned long PERGES_MS = 50;  // ennyi ideig kell stabilnak lennie a gombnak

bool ledBe = false;              // világít-e most a LED
int stabilAllapot = HIGH;        // a pergés nélküli, elfogadott gombállapot
int elozoNyers = HIGH;           // az előző loop()-ban olvasott érték
unsigned long utolsoValtas = 0;  // mikor változott utoljára a nyers érték

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(GOMB_PIN, INPUT_PULLUP);
}

void loop() {
  int nyers = digitalRead(GOMB_PIN);
  if (nyers != elozoNyers) {
    utolsoValtas = millis();  // még pereg: újraindul a várakozás
  }
  elozoNyers = nyers;

  if (millis() - utolsoValtas > PERGES_MS && nyers != stabilAllapot) {
    stabilAllapot = nyers;       // 50 ms óta nem változott: elfogadjuk
    if (stabilAllapot == LOW) {  // most nyomták le
      ledBe = !ledBe;            // átváltás: be -> ki, ki -> be
      digitalWrite(LED_BUILTIN, ledBe);
    }
  }
}
