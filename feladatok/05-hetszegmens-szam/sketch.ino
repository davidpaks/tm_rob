// 05 – Szám kiírása 7 szegmenses kijelzőre
// Közös katódos kijelző: a szegmens akkor világít, ha a lábára HIGH (1) kerül.

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

void setup() {
  pinMode(A, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(C, OUTPUT);
  pinMode(D, OUTPUT);
  pinMode(E, OUTPUT);
  pinMode(F, OUTPUT);
  pinMode(G, OUTPUT);
  display(5);  // ide írható a megjelenítendő számjegy
}

void loop() {
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
