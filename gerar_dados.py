# Gera um arquivo uf-XX.json por UF a partir do CSV do Censo Escolar.
# Uso: python3 gerar_dados.py base.csv pasta_saida
import sys, json, csv, os, locale
from collections import defaultdict
src, out = sys.argv[1], sys.argv[2]
DEPS = ["Municipal", "Estadual", "Federal", "Privada"]
por_uf = defaultdict(list)
with open(src, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        por_uf[r["estado"].strip()].append((r["municipio"].strip(), r["dependencia"].strip(),
                                             r["nome_escola"].strip(), r["inep"].strip()))
import unicodedata
def k(s): return unicodedata.normalize("NFD", s.lower()).encode("ascii","ignore").decode()
total = 0
for uf, rows in sorted(por_uf.items()):
    munis = sorted({r[0] for r in rows}, key=k)
    mi = {m: i for i, m in enumerate(munis)}
    rows.sort(key=lambda r: (k(r[0]), k(r[2])))
    esc = [[mi[m], DEPS.index(d), n, int(i)] for m, d, n, i in rows]
    with open(os.path.join(out, f"uf-{uf}.json"), "w", encoding="utf-8") as g:
        json.dump({"uf": uf, "d": DEPS, "m": munis, "e": esc}, g, ensure_ascii=False, separators=(",", ":"))
    total += len(esc)
print(len(por_uf), "UFs,", total, "escolas")
