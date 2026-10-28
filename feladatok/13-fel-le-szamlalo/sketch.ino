// 13 – Fel-le számláló: két nyomógomb és a 7 szegmenses kijelző
// A zöld gomb eggyel növeli, a piros eggyel csökkenti a kijelzett számot (0–9, körbe-körbe).
// Mindkét gombot a 11. feladat millis()-es pergésmentesítése kezeli. A két gomb adatai
// tömbökben vannak, így ugyanaz a lenyomtak() függvény mindkettőhöz használható.

const int A = 12;
const int B = 13;
const int C = 7;
const int D = 8;
const int E = 9;
const int F = 11;
const int G = 10;

// Melyik szegmens világít az egyes számjegyeknél (1 = világít).
//                            A  B  C  D  E  F  G
const int numArray[10][7] = {{1, 1, 1, 1, 1, 1, 0},  // 0
                             {0, 1, 1, 0, 0, 0, 0},  // 1
                             {1, 1, 0, 1, 1, 0, 1},  // 2
                             {1, 1, 1, 1, 0, 0, 1},  // 3
                             {0, 1, 1, 0, 0, 1, 1},  // 4
                             {1, 0, 1, 1, 0, 1, 1},  // 5
                             {1, 0, 1, 1, 1, 1, 1},  // 6
                             {1, 1, 1, 0, 0, 0, 0},  // 7
                             {1, 1, 1, 1, 1, 1, 1},  // 8
                             {1, 1, 1, 1, 0, 1, 1}}; // 9

// A gombok sorszáma a tömbökben.
const int FEL = 0;  // zöld gomb: növel
const int LE = 1;   // piros gomb: csökkent

const int GOMB_PIN[2] = {2, 3};
const unsigned long PERGES_MS = 50;  // ennyi ideig kell stabilnak lennie a gombnak

int stabilAllapot[2] = {HIGH, HIGH};    // a pergés nélküli, elfogadott gombállapot
int elozoNyers[2] = {HIGH, HIGH};       // az előző loop()-ban olvasott érték
unsigned long utolsoValtas[2] = {0, 0}; // mikor változott utoljára a nyers érték

int szam = 0;

void setup() {
  pinMode(A, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(C, OUTPUT);
  pinMode(D, OUTPUT);
  pinMode(E, OUTPUT);
  pinMode(F, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(GOMB_PIN[FEL], INPUT_PULLUP);
  pinMode(GOMB_PIN[LE], INPUT_PULLUP);
  display(szam);
}

void loop() {
  if (lenyomtak(FEL)) {
    szam++;
    if (szam > 9) {
      szam = 0;
    }
    display(szam);
  }
  if (lenyomtak(LE)) {
    szam--;
    if (szam < 0) {
      szam = 9;
    }
    display(szam);
  }
}

// Akkor ad vissza igazat (true), ha a megadott gombot éppen most nyomták le.
// Ugyanaz a pergésmentesítés, mint a 11. feladatban, csak a gomb sorszámával indexelt tömbökkel.
bool lenyomtak(int gomb) {
  int nyers = digitalRead(GOMB_PIN[gomb]);
  if (nyers != elozoNyers[gomb]) {
    utolsoValtas[gomb] = millis();  // még pereg: újraindul a várakozás
  }
  elozoNyers[gomb] = nyers;

  if (millis() - utolsoValtas[gomb] > PERGES_MS && nyers != stabilAllapot[gomb]) {
    stabilAllapot[gomb] = nyers;    // 50 ms óta nem változott: elfogadjuk
    if (stabilAllapot[gomb] == LOW) {
      return true;                  // most nyomták le
    }
  }
  return false;
}

// Megjeleníti a kapott számjegyet (0–9): a táblázat megfelelő sora szerint kapcsolja a szegmenseket.
void display(int szam) {
  digitalWrite(A, numArray[szam][0]);
  digitalWrite(B, numArray[szam][1]);
  digitalWrite(C, numArray[szam][2]);
  digitalWrite(D, numArray[szam][3]);
  digitalWrite(E, numArray[szam][4]);
  digitalWrite(F, numArray[szam][5]);
  digitalWrite(G, numArray[szam][6]);
}
