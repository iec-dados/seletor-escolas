# Gera um arquivo uf-XX.json por UF a partir do CSV do Censo Escolar
# e, se existir, do escolas_extras.csv (escolas novas, sem INEP).
# Uso: python3 gerar_dados.py base.csv pasta_saida [escolas_extras.csv]
#
# escolas_extras.csv: mesmas colunas da base (estado, municipio, dependencia,
# nome_escola, inep). No campo inep, use um código provisório começando com
# IEC (ex.: IEC-AL-0001). Quando a escola ganhar INEP, troque pelo código real.
import sys, json, csv, os, unicodedata
from collections import defaultdict

src, out = sys.argv[1], sys.argv[2]
extras = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "escolas_extras.csv")
DEPS = ["Municipal", "Estadual", "Federal", "Privada"]

por_uf = defaultdict(list)
vistos = set()

def ler(caminho, provisorio_ok):
    n = 0
    with open(caminho, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            uf, mun, dep = r["estado"].strip(), r["municipio"].strip(), r["dependencia"].strip()
            nome, cod = r["nome_escola"].strip(), r["inep"].strip()
            if not (uf and mun and nome and cod):
                continue
            if dep not in DEPS:
                sys.exit(f"Dependência inválida '{dep}' em {caminho}: use {DEPS}")
            if cod.isdigit():
                cod = int(cod)
            elif not (provisorio_ok and cod.upper().startswith("IEC")):
                sys.exit(f"Código inválido '{cod}' em {caminho}")
            if str(cod) in vistos:
                sys.exit(f"Código repetido: {cod}")
            vistos.add(str(cod))
            por_uf[uf].append((mun, dep, nome, cod))
            n += 1
    return n

base_n = ler(src, False)
extra_n = ler(extras, True) if os.path.exists(extras) else 0

def k(s): return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()

for uf, rows in sorted(por_uf.items()):
    munis = sorted({r[0] for r in rows}, key=k)
    mi = {m: i for i, m in enumerate(munis)}
    rows.sort(key=lambda r: (k(r[0]), k(r[2])))
    esc = [[mi[m], DEPS.index(d), n, c] for m, d, n, c in rows]
    with open(os.path.join(out, f"uf-{uf}.json"), "w", encoding="utf-8") as g:
        json.dump({"uf": uf, "d": DEPS, "m": munis, "e": esc}, g, ensure_ascii=False, separators=(",", ":"))

print(f"{len(por_uf)} UFs, {base_n} escolas da base + {extra_n} escolas extras")
