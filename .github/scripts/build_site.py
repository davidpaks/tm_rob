"""A GitHub Pages oldal összerakása a feladatok mappából és a tananyag.json-ból.

- A tananyag.json mondja meg, melyik feladat melyik tanegységhez tartozik.
- Feladatonként a README.md adja a leírást, a diagram.json-ból generálódik
  az alkatrészlista, a bekötési táblázat és a bekötési ábra (wokwi-elements).
- A sketch.ino színezve (Pygments, Arduino-lexer) jelenik meg a mintamegoldásnál.
- Minden feladathoz letölthető .zip készül (sketch.ino + diagram.json), ami
  Wokwi-projektként megnyitható.

Futtatás:  python3 .github/scripts/build_site.py  [kimeneti mappa, alapból _site]
Függőség:  pip install markdown pygments
"""
import html
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import ArduinoLexer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "feladatok"
DATA = json.loads((ROOT / "tananyag.json").read_text(encoding="utf-8"))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
REPO_URL = "https://github.com/davidpaks/tm_rob"
WOKWI_ELEMENTS = "https://cdn.jsdelivr.net/npm/@wokwi/elements@1.9.2/dist/wokwi-elements.bundle.min.js"
PUBLISHED = ["README.md", "sketch.ino", "diagram.json", "teszt.yaml", "wokwi.toml"]
ZIPPED = ["sketch.ino", "diagram.json"]
e = html.escape

# --- a diagram.json magyar megnevezései ---

SZINEK = {
    "red": "piros", "green": "zöld", "blue": "kék", "yellow": "sárga", "orange": "narancs",
    "white": "fehér", "black": "fekete", "gray": "szürke", "grey": "szürke", "purple": "lila",
    "violet": "ibolya", "brown": "barna", "cyan": "türkiz", "magenta": "bíbor",
    "limegreen": "világoszöld", "gold": "arany",
}
TIPUSOK = {
    "wokwi-arduino-uno": "Arduino Uno",
    "wokwi-led": "LED",
    "wokwi-resistor": "ellenállás",
    "wokwi-pushbutton": "nyomógomb",
    "wokwi-potentiometer": "potméter",
    "wokwi-slide-potentiometer": "tolópotméter",
    "wokwi-lcd1602": "16×2 LCD",
    "wokwi-buzzer": "zümmer",
    "wokwi-breadboard": "próbapanel",
    "wokwi-breadboard-half": "próbapanel (fél méretű, 30 oszlopos)",
    "wokwi-breadboard-mini": "mini próbapanel",
}
SINEK = {"tp": "felső + sín", "tn": "felső − sín", "bp": "alsó + sín", "bn": "alsó − sín"}
LABAK = {
    "wokwi-led": {"A": "anód (+)", "C": "katód (−)"},
    "wokwi-resistor": {"1": "1. láb", "2": "2. láb"},
    "wokwi-potentiometer": {"GND": "GND", "SIG": "csúszka (SIG)", "VCC": "VCC"},
}


def ohm(value: str) -> str:
    try:
        v = float(value)
    except ValueError:
        return f"{value} Ω"
    for div, unit in ((1e6, "MΩ"), (1e3, "kΩ")):
        if v >= div:
            return f"{v / div:g} {unit}".replace(".", ",")
    return f"{v:g} Ω".replace(".", ",")


def describe(p: dict) -> str:
    """Egy alkatrész rövid, típus szerinti leírása (pl. 'piros LED', '220 Ω-os ellenállás')."""
    t, attrs = p["type"], p.get("attrs", {})
    name = TIPUSOK.get(t, t.removeprefix("wokwi-"))
    if t == "wokwi-led":
        return f"{SZINEK.get(attrs.get('color', 'red'), attrs.get('color'))} LED"
    if t == "wokwi-resistor":
        return f"{ohm(attrs.get('value', '1000'))}-os ellenállás"
    return name


def part_names(parts: list[dict]) -> dict[str, str]:
    """Alkatrész-azonosító -> a táblázatban használt név. Az ellenállás az azonosítóját
    kapja (R1), a többi a leírását; ha a leírás nem egyedi, mögé kerül az azonosító."""
    names = {}
    for p in parts:
        t = p["type"]
        if t == "wokwi-arduino-uno":
            names[p["id"]] = "Arduino"
        elif is_breadboard(t):
            names[p["id"]] = "próbapanel"
        elif t == "wokwi-resistor":
            names[p["id"]] = f"{p['id'].upper()} ({ohm(p.get('attrs', {}).get('value', '1000'))})"
        else:
            names[p["id"]] = describe(p)
    counts = {}
    for n in names.values():
        counts[n] = counts.get(n, 0) + 1
    return {i: (f"{n} ({i})" if counts[n] > 1 else n) for i, n in names.items()}


def is_breadboard(part_type: str) -> bool:
    return part_type.startswith("wokwi-breadboard")


def is_bb_connection(conn: list) -> bool:
    """A Wokwi így jelöli, ha egy alkatrész lába közvetlenül a próbapanelbe van dugva."""
    return len(conn) > 3 and conn[3] == ["$bb"]


def pin_label(part_type: str, pin: str) -> str:
    if part_type == "wokwi-arduino-uno":
        if pin.isdigit():
            return f"D{pin}"
        return pin.split(".")[0]  # GND.1 -> GND
    if is_breadboard(part_type):
        hole, rail = pin.split(".")
        if hole in SINEK:
            return SINEK[hole]  # bn.6 -> alsó − sín
        return f"{rail}{hole[:-1]}"  # 13b.j -> j13
    return LABAK.get(part_type, {}).get(pin, pin)


def parts_list(diagram: dict) -> str:
    counts: dict[str, int] = {}
    for p in diagram["parts"]:
        d = describe(p)
        counts[d] = counts.get(d, 0) + 1
    wires = sum(1 for c in diagram["connections"] if not is_bb_connection(c))
    if wires and any(is_breadboard(p["type"]) for p in diagram["parts"]):
        counts["vezeték (jumper)"] = wires
    return "".join(f"<li>{n} db {e(d)}</li>" for d, n in counts.items())


def placement_table(diagram: dict) -> str:
    """Melyik alkatrész melyik lába melyik próbapanel-lyukba kerül."""
    types = {p["id"]: p["type"] for p in diagram["parts"]}
    names = part_names(diagram["parts"])
    holes: dict[str, list[str]] = {}
    for a, b, *_ in filter(is_bb_connection, diagram["connections"]):
        pid, pin = a.split(":", 1)
        bid, hole = b.split(":", 1)
        holes.setdefault(pid, []).append(
            f"{e(pin_label(types[pid], pin))} → <strong>{e(pin_label(types[bid], hole))}</strong>")
    if not holes:
        return ""
    rows = "".join(f"<tr><td>{e(names[pid])}</td><td>{', '.join(h)}</td></tr>" for pid, h in holes.items())
    return ('<h3>Elhelyezés a próbapanelen</h3><div class="table-scroll"><table class="wiring placement">'
            "<thead><tr><th>Alkatrész</th><th>Lábak helye</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></div>")


def wiring_table(diagram: dict) -> str:
    types = {p["id"]: p["type"] for p in diagram["parts"]}
    names = part_names(diagram["parts"])

    def end(ref: str) -> str:
        pid, pin = ref.split(":", 1)
        return f"{e(names[pid])} – <strong>{e(pin_label(types[pid], pin))}</strong>"

    wires = [c for c in diagram["connections"] if not is_bb_connection(c)]
    rows = "".join(
        f"<tr><td>{i}.</td><td>{end(a)}</td><td>{end(b)}</td>"
        f'<td><span class="wire" style="background:{e(color)}"></span>{e(SZINEK.get(color, color))}</td></tr>'
        for i, (a, b, color, *_) in enumerate(wires, 1))
    return ('<h3>Vezetékek</h3><div class="table-scroll"><table class="wiring"><thead><tr><th></th><th>Honnan</th>'
            f"<th>Hova</th><th>Vezeték</th></tr></thead><tbody>{rows}</tbody></table></div>")


# --- README ---

def read_readme(task: Path) -> tuple[str, str]:
    """(cím, html) – a cím az első # sor, a sorszám nélkül."""
    text = (task / "README.md").read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)\n", text)
    title = m.group(1).strip() if m else task.name
    title = re.sub(r"^\d+\s*[–-]\s*", "", title)
    body = text[m.end():] if m else text
    return title, markdown.markdown(body, extensions=["tables"])


def number(task: Path) -> str:
    return task.name.split("-")[0].lstrip("0") or "0"


ICON_DL = '<svg aria-hidden="true" viewBox="0 0 16 16"><path d="M8 2v8m0 0-3-3m3 3 3-3M3 13h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_OPEN = '<svg aria-hidden="true" viewBox="0 0 16 16"><path d="M9 3h4v4m0-4L7 9M11 10v3H3V5h3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

DARK = """
  --paper:#0f1626; --sheet:#162036; --ink:#e6ebf5; --muted:#9aa6c0; --line:#2a3754;
  --cobalt:#8fb0ff; --cobalt-soft:#1e2c4d; --teal:#6fd3c0; --teal-soft:#15332f;
  color-scheme:dark;
"""

CSS = """
:root{
  --paper:#f2f5f9; --sheet:#ffffff; --ink:#14213d; --muted:#56607a; --line:#d6dde8;
  --cobalt:#2b59c3; --cobalt-soft:#e4ecfb; --teal:#0e6b5c; --teal-soft:#e0f1ed;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"Atkinson Hyperlegible",system-ui,-apple-system,"Segoe UI",sans-serif;
  color-scheme:light;
}
/* sötét mód: a rendszerbeállítás szerint, vagy ha a téma gombbal kézzel választották */
:root[data-theme="dark"]{DARK}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){DARK}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 var(--sans)}
a{color:var(--cobalt);text-underline-offset:3px}
a:focus-visible,summary:focus-visible{outline:3px solid var(--cobalt);outline-offset:2px;border-radius:4px}
.wrap{max-width:880px;margin:0 auto;padding:0 16px}
code,.chip,pre{font-family:var(--mono);font-size:.82em}

/* fejléc */
.hero{padding:56px 0 40px;border-bottom:1px solid var(--line)}
.hero h1{font-size:clamp(2.1rem,6vw,3.1rem);line-height:1.1;margin:0 0 .6rem;letter-spacing:-.01em}
.hero h1 .tag{color:var(--muted);font-family:var(--mono);font-weight:400;font-size:.62em;vertical-align:.18em}
.hero p{margin:0;max-width:62ch;color:var(--muted)}
.path{list-style:none;margin:28px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.path li{display:flex;align-items:center;font-size:.9rem;color:var(--muted)}
.path span{padding:4px 10px;border-radius:999px;border:1px dashed var(--line)}
.path .kesz span{border:1px solid transparent;background:var(--teal-soft);color:var(--teal);font-weight:700}
.path-note{margin:10px 0 0;font-size:.85rem;color:var(--muted)}

/* órák */
.lessons{list-style:none;margin:0;padding:8px 0 48px}
.lesson{display:grid;grid-template-columns:72px 1fr;gap:0 20px;padding:36px 0;border-bottom:1px solid var(--line)}
.lesson:last-child{border-bottom:0}
.num{font-size:3.2rem;line-height:1;font-weight:700;color:var(--cobalt);font-variant-numeric:tabular-nums}
.num small{display:block;font-size:.8rem;font-weight:400;color:var(--muted);margin-top:4px}
.lesson h2{font-size:1.45rem;line-height:1.25;margin:4px 0 12px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px;padding:0;list-style:none}
.chip{background:var(--teal-soft);color:var(--teal);padding:2px 8px;border-radius:5px;white-space:nowrap}
.tasks{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.task{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 16px;padding:14px 0;border-bottom:1px solid var(--line)}
.task-name{font-weight:700;font-size:1.08rem}
.task-name a{color:var(--ink);text-decoration:none}
.task-name a:hover{color:var(--cobalt);text-decoration:underline}
.task-no{color:var(--muted);font-weight:400;font-variant-numeric:tabular-nums;margin-right:6px}
.role{display:inline-block;font-size:.78rem;font-weight:700;padding:1px 8px;border-radius:999px;margin-right:8px;vertical-align:.12em}
.role-órai{background:var(--cobalt);color:var(--sheet)}
.role-gyakorló{border:1px solid var(--cobalt);color:var(--cobalt)}
.note{display:block;font-weight:400;font-size:.9rem;color:var(--muted);margin-top:2px}
.actions{display:flex;flex-wrap:wrap;gap:8px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:7px;font-size:.9rem;font-weight:700;text-decoration:none;background:var(--cobalt-soft);color:var(--cobalt)}
.btn:hover{background:var(--cobalt);color:var(--sheet)}
.btn svg{width:15px;height:15px}

/* feladatoldal */
.crumb{display:inline-block;margin:32px 0 0;font-size:.95rem}
.task-hero{padding:16px 0 28px;border-bottom:1px solid var(--line)}
.task-hero h1{font-size:clamp(1.9rem,5vw,2.6rem);line-height:1.15;margin:0 0 .5rem}
.where{margin:0;padding:0;list-style:none;color:var(--muted)}
.steps{counter-reset:s;list-style:none;margin:28px 0 8px;padding:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.steps li{counter-increment:s;padding:14px 16px 14px 52px;position:relative;background:var(--sheet);border:1px solid var(--line);border-radius:10px;font-size:.95rem}
.steps li::before{content:counter(s);position:absolute;left:16px;top:12px;width:24px;height:24px;border-radius:50%;background:var(--cobalt);color:var(--sheet);font-weight:700;font-size:.85rem;display:grid;place-items:center}
.section{margin:28px 0;background:var(--sheet);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.section.solution{border-color:var(--cobalt)}
.section>h2{font-size:1.2rem;margin:0 0 12px}
.section-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:12px}
.section-head h2{font-size:1.2rem;margin:0}
.section h3{font-size:1rem;margin:20px 0 6px}
.readme h2{font-size:1.1rem;margin:20px 0 6px}
.readme h2:first-child{margin-top:0}
.readme table,.wiring{border-collapse:collapse;width:100%;font-size:.95rem}
.readme th,.readme td,.wiring th,.wiring td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.wiring td:first-child{color:var(--muted);width:2.5em;font-variant-numeric:tabular-nums}
.placement td:first-child{color:var(--ink);width:auto;white-space:nowrap}
.table-scroll{overflow-x:auto}
.wire{display:inline-block;width:22px;height:6px;border-radius:3px;margin-right:8px;vertical-align:.15em;box-shadow:0 0 0 1px var(--line)}
.parts{margin:0;padding-left:1.2em}
.figure{position:relative;overflow:hidden;margin:0 0 16px;border-radius:8px;background:#f7f7f2}
.figure .stage{position:absolute;left:0;top:0;transform-origin:0 0}
.figure .stage>*{position:absolute;line-height:0}
.figure svg.wires{overflow:visible;pointer-events:none}
.figure-note{margin:0 0 16px;font-size:.85rem;color:var(--muted)}

/* kód */
.codebox{margin:4px 0 0;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.codebar{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:6px 8px 6px 14px;background:var(--paper);border-bottom:1px solid var(--line);font-family:var(--mono);font-size:.82rem;color:var(--muted)}
.copy{font:inherit;font-family:var(--sans);font-weight:700;font-size:.85rem;padding:4px 10px;border:0;border-radius:6px;background:var(--cobalt-soft);color:var(--cobalt);cursor:pointer}
.copy:hover{background:var(--cobalt);color:var(--sheet)}
.copy:focus-visible{outline:3px solid var(--cobalt);outline-offset:2px}
.hl{overflow-x:auto}
.hl pre{margin:0;padding:14px 16px;background:none;border:0;line-height:1.55;font-size:.86rem}
/* téma gomb */
.topbar{position:relative;height:0}
.theme-toggle{position:absolute;top:14px;right:16px;z-index:1;display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border:1px solid var(--line);border-radius:999px;background:var(--sheet);color:var(--ink);font:inherit;font-size:.85rem;cursor:pointer}
.theme-toggle:hover{border-color:var(--cobalt);color:var(--cobalt)}
.theme-toggle:focus-visible{outline:3px solid var(--cobalt);outline-offset:2px}
.theme-toggle svg{width:16px;height:16px}
.hl .linenos{display:inline-block;min-width:2em;margin-right:14px;text-align:right;color:var(--muted);opacity:.7;user-select:none}
footer{border-top:1px solid var(--line);padding:24px 0 48px;color:var(--muted);font-size:.9rem}

@media (max-width:560px){
  .lesson{grid-template-columns:1fr}
  .num{font-size:2.2rem;display:flex;align-items:baseline;gap:8px;margin-bottom:6px}
  .num small{display:inline;margin:0}
  .hero{padding-top:36px}
  .section{padding:14px}
}
"""

# A bekötési ábra: a diagram.json alkatrészeit wokwi-elements komponensként helyezi el,
# a vezetékeket egy SVG-rétegre rajzolja (a Wokwi-féle 'v'/'h' útvonal-utasításokkal).
FIGURE_JS = """
const PAD = 24;
const NS = 'http://www.w3.org/2000/svg';

// A wokwi-elements nem tartalmaz próbapanelt, ezért ez a Wokwi-szerkesztő fél próbapanelét
// rajzolja újra, azonos lyukkiosztással (9,6 px-es raszter, 30 oszlop, sínenként 25 lyuk).
const P = 9.6;
const BB_ROWS = 'abcdefghij';
const BB_RAILS = { tp: 12.3, tn: 22.3, bp: 186.3, bn: 196.3 };
class BreadboardHalf extends HTMLElement {
  updateComplete = Promise.resolve();

  get pinInfo() {
    const pins = [];
    [...BB_ROWS].forEach((row, t) => {
      const y = 51 + t * P + (t >= 5 ? 2 * P : 0);
      for (let c = 1; c <= 30; c++) pins.push({ name: `${c}${t >= 5 ? 'b' : 't'}.${row}`, x: 26 + (c - 1) * P, y });
    });
    for (const [rail, y] of Object.entries(BB_RAILS)) {
      for (let r = 0; r < 25; r++) pins.push({ name: `${rail}.${r + 1}`, x: 34 + r * P + Math.floor(r / 5) * P, y });
    }
    return pins;
  }

  connectedCallback() {
    const holes = this.pinInfo.map((p) => `<rect x="${p.x - 1.9}" y="${p.y - 1.9}" width="3.8" height="3.8" rx=".6"/>`);
    const label = (x, y, s) => `<text x="${x}" y="${y}">${s}</text>`;
    const letters = [...BB_ROWS].flatMap((r, t) => {
      const y = 53.5 + t * P + (t >= 5 ? 2 * P : 0);
      return [label(14, y, r), label(312, y, r)];
    });
    const numbers = [1, 5, 10, 15, 20, 25, 30].flatMap((c) => {
      const x = 26 + (c - 1) * P - (c < 10 ? 2 : 4);
      return [label(x, 43, c), label(x, 169, c)];
    });
    const line = (y, color) => `<rect x="36.5" y="${y}" width="264.6" height="1" fill="${color}" opacity=".7"/>`;
    this.innerHTML = `<svg xmlns="${NS}" width="328.8" height="207.9" viewBox="0 0 328.8 207.9" style="display:block">
      <rect width="328.8" height="207.9" rx="3" fill="${this.getAttribute('color') || '#eeefed'}"/>
      <rect x="5.7" y="100" width="317.5" height="7" fill="#e3e3e3"/>
      ${line(5, '#F97466')}${line(30, '#55d2fd')}${line(176, '#F97466')}${line(203, '#55d2fd')}
      <g fill="#555" opacity=".55">${holes.join('')}</g>
      <g font-size="7" font-family="sans-serif" fill="#000" opacity=".55">${letters.join('')}${numbers.join('')}</g>
      <g font-size="10" font-family="sans-serif" font-weight="bold">
        <text x="12" y="16" fill="#F97466">+</text><text x="12" y="26" fill="#55d2fd">−</text>
        <text x="12" y="190" fill="#F97466">+</text><text x="12" y="200" fill="#55d2fd">−</text>
      </g></svg>`;
  }
}
customElements.define('wokwi-breadboard-half', BreadboardHalf);

function rotate([x, y], [cx, cy], deg) {
  const r = deg * Math.PI / 180, c = Math.cos(r), s = Math.sin(r);
  return [cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c];
}

function route(start, hints) {
  const pts = [start];
  for (const h of hints) {
    const [x, y] = pts[pts.length - 1], d = parseFloat(h.slice(1));
    if (h[0] === 'v') pts.push([x, y + d]);
    else if (h[0] === 'h') pts.push([x + d, y]);
  }
  return pts;
}

async function draw(fig) {
  const diagram = JSON.parse(fig.querySelector('script').textContent);
  const stage = document.createElement('div');
  stage.className = 'stage';
  fig.append(stage);

  const parts = {};
  for (const p of diagram.parts) {
    const el = document.createElement(p.type);
    for (const [k, v] of Object.entries(p.attrs || {})) el.setAttribute(k, v);
    Object.assign(el.style, { left: p.left + 'px', top: p.top + 'px' });
    if (p.rotate) el.style.transform = `rotate(${p.rotate}deg)`;
    stage.append(el);
    parts[p.id] = { el, p };
  }
  await Promise.all(Object.values(parts).map(({ el }) => el.updateComplete));

  const xs = [], ys = [];
  const add = ([x, y]) => { xs.push(x); ys.push(y); };
  for (const { el, p } of Object.values(parts)) {
    const w = el.offsetWidth, h = el.offsetHeight, c = [w / 2, h / 2];
    for (const q of [[0, 0], [w, 0], [0, h], [w, h]]) {
      const [x, y] = rotate(q, c, p.rotate || 0);
      add([p.left + x, p.top + y]);
    }
  }
  const pin = (ref) => {
    const [id, name] = [ref.slice(0, ref.indexOf(':')), ref.slice(ref.indexOf(':') + 1)];
    const { el, p } = parts[id];
    const info = el.pinInfo.find((i) => i.name === name);
    const [x, y] = rotate([info.x, info.y], [el.offsetWidth / 2, el.offsetHeight / 2], p.rotate || 0);
    return [p.left + x, p.top + y];
  };

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'wires');
  svg.setAttribute('width', '1');
  svg.setAttribute('height', '1');
  for (const [a, b, color, hints = []] of diagram.connections) {
    if (hints.length === 1 && hints[0] === '$bb') continue;  // a próbapanelbe dugott láb, nem vezeték
    const star = hints.indexOf('*');
    const fromA = route(pin(a), star < 0 ? hints : hints.slice(0, star));
    const fromB = star < 0 ? [pin(b)] : route(pin(b), hints.slice(star + 1).reverse()).reverse();
    const pts = [...fromA, ...fromB];
    pts.forEach(add);
    const line = document.createElementNS(NS, 'polyline');
    line.setAttribute('points', pts.map((q) => q.join(',')).join(' '));
    Object.entries({ fill: 'none', stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' })
      .forEach(([k, v]) => line.setAttribute(k, v));
    svg.append(line);
  }
  stage.append(svg);

  const minX = Math.min(...xs) - PAD, minY = Math.min(...ys) - PAD;
  const w = Math.max(...xs) + PAD - minX, h = Math.max(...ys) + PAD - minY;
  const fit = () => {
    const scale = Math.min(1.6, fig.clientWidth / w);
    stage.style.transform = `scale(${scale}) translate(${-minX}px, ${-minY}px)`;
    fig.style.height = h * scale + 'px';
  };
  fit();
  new ResizeObserver(fit).observe(fig);
}

document.querySelectorAll('.figure').forEach(draw);
"""

def highlight_ino(code: str) -> str:
    return highlight(code, ArduinoLexer(), HtmlFormatter(cssclass="hl", linenos="inline"))


def code_css() -> str:
    """Világos módban az Arduino IDE színei, sötét módban a GitHub sötét témája."""
    def defs(style: str, prefix: str) -> str:
        f = HtmlFormatter(style=style)
        return "\n".join(f.get_background_style_defs(prefix) + f.get_token_style_defs(prefix))
    return (defs("arduino", ".hl") + "\n"
            + defs("github-dark", ':root[data-theme="dark"] .hl')
            + "\n@media (prefers-color-scheme:dark){\n"
            + defs("github-dark", ':root:not([data-theme="light"]) .hl') + "\n}\n")


# Másolás gomb: a sorszámok nélkül teszi a vágólapra a kódot.
COPY_JS = """
document.querySelectorAll('.codebox').forEach((box) => {
  const btn = box.querySelector('.copy');
  btn.addEventListener('click', async () => {
    const pre = box.querySelector('pre').cloneNode(true);
    pre.querySelectorAll('.linenos').forEach((n) => n.remove());
    try {
      await navigator.clipboard.writeText(pre.textContent);
      btn.textContent = 'Másolva';
    } catch {
      btn.textContent = 'Nem sikerült';
    }
    setTimeout(() => { btn.textContent = 'Másolás'; }, 1500);
  });
});
"""

# Téma gomb: világos és sötét mód között vált; a választást a böngésző megjegyzi.
# A <head>-ben lévő rövid szkript még a rajzolás előtt beállítja, hogy ne villanjon.
THEME_HEAD = ("<script>try{var t=localStorage.getItem('tema');"
              "if(t)document.documentElement.dataset.theme=t}catch(e){}</script>")
ICON_MOON = '<svg aria-hidden="true" viewBox="0 0 16 16"><path d="M13.5 9.5A5.5 5.5 0 0 1 6.5 2.5a5.5 5.5 0 1 0 7 7Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>'
ICON_SUN = '<svg aria-hidden="true" viewBox="0 0 16 16"><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5v1.5M8 13v1.5M1.5 8H3M13 8h1.5M3.4 3.4l1 1M11.6 11.6l1 1M3.4 12.6l1-1M11.6 4.4l1-1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
THEME_JS = """
const root = document.documentElement;
const btn = document.querySelector('.theme-toggle');
const system = matchMedia('(prefers-color-scheme: dark)');
const current = () => root.dataset.theme || (system.matches ? 'dark' : 'light');

function render() {
  const dark = current() === 'dark';
  btn.innerHTML = (dark ? '%SUN%' : '%MOON%') + `<span>${dark ? 'Világos mód' : 'Sötét mód'}</span>`;
  btn.setAttribute('aria-label', dark ? 'Váltás világos módra' : 'Váltás sötét módra');
}

btn.addEventListener('click', () => {
  root.dataset.theme = current() === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('tema', root.dataset.theme); } catch (e) {}
  render();
});
system.addEventListener('change', render);
render();
""".replace("%SUN%", ICON_SUN).replace("%MOON%", ICON_MOON)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700'
         '&family=JetBrains+Mono:wght@400&display=swap">')


def page(title: str, body: str, base: str, scripts: str = "") -> str:
    return f"""<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
{THEME_HEAD}
{FONTS}
<link rel="stylesheet" href="{base}assets/oldal.css">
</head>
<body>
<div class="wrap topbar"><button class="theme-toggle" type="button">Téma</button></div>
{body}
<footer><div class="wrap">A feladatok forrásfájljai a <a href="{REPO_URL}">tm_rob GitHub repositoryban</a> is elérhetők.</div></footer>
<script src="{base}assets/tema.js"></script>
{scripts}
</body>
</html>
"""


def zip_name(task: Path) -> str:
    return f"{task.name}.zip"


def task_row(task: Path, title: str, role: str | None, note: str | None) -> str:
    btns = (f'<a class="btn" href="feladatok/{task.name}/">{ICON_OPEN}Feladat</a>'
            f'<a class="btn" href="feladatok/{task.name}/{zip_name(task)}" download>{ICON_DL}Wokwi-projekt</a>')
    role_html = f'<span class="role role-{role}">{"Órai" if role == "órai" else "Gyakorló"}</span>' if role else ""
    note_html = f'<span class="note">{e(note)}</span>' if note else ""
    return (f'<li class="task"><div class="task-name">{role_html}<span class="task-no">{number(task)}.</span>'
            f'<a href="feladatok/{task.name}/">{e(title)}</a>{note_html}</div>'
            f'<div class="actions">{btns}</div></li>')


def task_page(task: Path, title: str, readme_html: str, lessons: list) -> str:
    diagram = json.loads((task / "diagram.json").read_text(encoding="utf-8"))
    code = (task / "sketch.ino").read_text(encoding="utf-8")

    where = "".join(
        f'<li>{i}. tanegység ({"órai" if f["szerep"] == "órai" else "gyakorló"} feladat): {e(ora["cim"])}'
        + (f' – {e(f["megjegyzes"])}' if f.get("megjegyzes") else "") + "</li>"
        for i, ora, f in lessons)
    where_html = f'<ul class="where">{where}</ul>' if where else ""
    steps = ('<ol class="steps"><li>A feladat leírásának és a bekötésnek az áttekintése.</li>'
             '<li>Az áramkör összeállítása (Wokwi-ban vagy valódi eszközökkel) és a program megírása.</li>'
             '<li>Összevetés a mintamegoldással.</li></ol>')

    diagram_json = json.dumps(diagram, ensure_ascii=False).replace("</", "<\\/")
    figure = (f'<div class="figure" role="img" aria-label="Bekötési ábra: {e(title)}">'
              f'<script type="application/json">{diagram_json}</script></div>'
              '<p class="figure-note">Az ábra a diagram.json alapján készül; a vezetékek elrendezése '
              'eltérhet a Wokwi-szerkesztőben látottól.</p>')
    if diagram["connections"]:
        wiring = figure + placement_table(diagram) + wiring_table(diagram)
    else:
        wiring = f"{figure}<p>Ehhez a feladathoz nincs szükség külső bekötésre.</p>"

    files = "".join(
        f'<a class="btn" href="{f}" download>{ICON_DL}{f}</a>' for f in ZIPPED)
    body = (
        f'<main class="wrap"><a class="crumb" href="../../">← Vissza a tanegységekhez</a>'
        f'<header class="task-hero"><h1>{number(task)}. {e(title)}</h1>{where_html}{steps}</header>'
        f'<section class="section readme">{readme_html}</section>'
        f'<section class="section"><h2>Alkatrészek</h2><ul class="parts">{parts_list(diagram)}</ul></section>'
        f'<section class="section"><h2>Bekötés</h2>{wiring}</section>'
        f'<section class="section solution" id="mintamegoldas"><div class="section-head"><h2>Mintamegoldás</h2>'
        f'<div class="actions"><a class="btn" href="{zip_name(task)}" download>{ICON_DL}Wokwi-projekt (.zip)</a>'
        f'{files}</div></div>'
        f'<div class="codebox"><div class="codebar"><span>sketch.ino</span>'
        f'<button class="copy" type="button">Másolás</button></div>{highlight_ino(code)}</div></section>'
        "</main>")
    scripts = (f'<script src="{WOKWI_ELEMENTS}"></script>'
               '<script src="../../assets/bekotes.js"></script><script src="../../assets/kod.js"></script>')
    return page(f"{number(task)}. {title} – {DATA['cim']}", body, "../../", scripts)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    css = CSS.replace("{DARK}", "{" + DARK + "}")
    (OUT / "assets" / "oldal.css").write_text(css.strip() + "\n\n" + code_css(), encoding="utf-8")
    (OUT / "assets" / "tema.js").write_text(THEME_JS.strip() + "\n", encoding="utf-8")
    (OUT / "assets" / "kod.js").write_text(COPY_JS.strip() + "\n", encoding="utf-8")
    (OUT / "assets" / "bekotes.js").write_text(FIGURE_JS.strip() + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("")

    tasks = {d.name: d for d in sorted(SRC.iterdir()) if d.is_dir()}
    lessons_of: dict[str, list[tuple[int, dict, dict]]] = {}
    for i, ora in enumerate(DATA["orak"], 1):
        for f in ora["feladatok"]:
            if f["mappa"] not in tasks:
                sys.exit(f"HIBA: a tananyag.json-ban szereplő '{f['mappa']}' mappa nincs a feladatok alatt.")
            lessons_of.setdefault(f["mappa"], []).append((i, ora, f))

    # --- feladatonkénti oldalak ---
    titles = {}
    for name, task in tasks.items():
        dest = OUT / "feladatok" / name
        dest.mkdir(parents=True)
        for f in PUBLISHED:
            if (task / f).exists():
                shutil.copy2(task / f, dest / f)
        with zipfile.ZipFile(dest / zip_name(task), "w", zipfile.ZIP_DEFLATED) as zf:
            for f in ZIPPED:
                zf.write(task / f, f"{name}/{f}")
        titles[name], readme_html = read_readme(task)
        (dest / "index.html").write_text(
            task_page(task, titles[name], readme_html, lessons_of.get(name, [])), encoding="utf-8")

    # --- főoldal ---
    path = "".join(
        f'<li class="{s["allapot"]}"><span>{e(s["nev"])}</span></li>' for s in DATA["tanulasi_ut"])
    lessons = []
    for i, ora in enumerate(DATA["orak"], 1):
        chips = "".join(f'<li class="chip">{e(k)}</li>' for k in ora.get("kulcsszavak", []))
        rows = "".join(task_row(tasks[f["mappa"]], titles[f["mappa"]], f["szerep"], f.get("megjegyzes"))
                       for f in ora["feladatok"])
        lessons.append(
            f'<li class="lesson"><div class="num">{i}.<small>tanegység</small></div><div>'
            f'<h2>{e(ora["cim"])}</h2><ul class="chips" aria-label="Új elemek">{chips}</ul>'
            f'<ul class="tasks">{rows}</ul></div></li>')
    extra = [n for n in tasks if n not in lessons_of]
    if extra:
        rows = "".join(task_row(tasks[n], titles[n], None, None) for n in extra)
        lessons.append(f'<li class="lesson"><div class="num">+</div><div><h2>További feladatok</h2>'
                       f'<ul class="tasks">{rows}</ul></div></li>')

    body = (f'<header class="hero"><div class="wrap">'
            f'<h1><span class="tag">loop()</span> {e(DATA["cim"])}</h1><p>{e(DATA["alcim"])}</p>'
            f'<ol class="path" aria-label="A tárgy témakörei">{path}</ol>'
            f'<p class="path-note">Kiemelve az eddig vett témakörök.</p></div></header>'
            f'<main class="wrap"><ol class="lessons">{"".join(lessons)}</ol></main>')
    (OUT / "index.html").write_text(page(DATA["cim"], body, ""), encoding="utf-8")
    print(f"{len(DATA['orak'])} tanegység, {len(tasks)} feladat -> {OUT}")


if __name__ == "__main__":
    build()
