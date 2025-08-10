#!/usr/bin/env python3
"""Gera propostas HTML a partir de arquivos YAML e templates Jinja2.
Uso: python gerar.py <slug_cliente>
Requisitos: pip install pyyaml jinja2
"""
import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import re

DATA_DIR = Path('data')
TEMPLATES_DIR = Path('templates_jinja')
OUTPUT_DIR = Path('output')

DEFAULT_FILE = DATA_DIR / '_defaults.yml'


def deep_merge(a: dict, b: dict) -> dict:
    """Merge recursivo: valores de b sobrepõem a em conflito."""
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_context(slug: str) -> dict:
    client_file = DATA_DIR / f'{slug}.yml'
    if not client_file.exists():
        sys.exit(f'Arquivo de cliente não encontrado: {client_file}')

    with DEFAULT_FILE.open() as f:
        base = yaml.safe_load(f)
    with client_file.open() as f:
        client = yaml.safe_load(f)

    context = deep_merge(base, client)

    # Adiciona slug do cliente
    nome = context['cliente']['nome']
    slug = re.sub(r'\s+', '-', nome.strip().lower())
    context['cliente_slug'] = slug
    return context


def render(slug: str, context: dict):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('base.html')
    html = template.render(**context)

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_file = OUTPUT_DIR / f'{slug}.html'
    out_file.write_text(html, encoding='utf-8')
    print(f'Proposta gerada: {out_file}')


def main():
    if len(sys.argv) != 2:
        print('Uso: python gerar.py <slug_cliente>')
        sys.exit(1)
    slug = sys.argv[1]
    context = load_context(slug)
    render(slug, context)


if __name__ == '__main__':
    main()
