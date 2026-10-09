#!/usr/bin/env python3
"""Troca o usuário do GitHub (padrão: pauloccoimbra) por outro em todos os arquivos de texto.

Uso:  python scripts/definir_usuario.py meu-usuario
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("Uso: python scripts/definir_usuario.py NOVO_USUARIO")
novo = sys.argv[1].strip()
raiz = Path(__file__).resolve().parent.parent
ANTIGO = "pauloccoimbra"
exts = {".md", ".html", ".ipynb", ".cff", ".py", ".txt", ".bib", ".css", ".js"}
n = 0
for f in raiz.rglob("*"):
    if f.is_file() and f.suffix in exts and ".git" not in f.parts and f.name != "definir_usuario.py":
        try:
            t = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if ANTIGO in t:
            f.write_text(t.replace(ANTIGO, novo), encoding="utf-8")
            n += 1
print(f"Pronto: {n} arquivo(s) atualizado(s) com o usuário '{novo}'.")
