#!/usr/bin/env python3
"""Extrai objeto JSON `content` de um HTML da proposta original e grava YAML.
Uso: python scripts/extrair_json.py <html_file> <slug>
Exemplo: python scripts/extrair_json.py original_pessoa.html thiago-pessoa
"""
import sys, re, json, yaml
from pathlib import Path

def extract_content(path: Path) -> dict:
    text = path.read_text(encoding='utf-8', errors='ignore')
    # procura a chave content:
    m = re.search(r"content\s*:\s*\{", text)
    if not m:
        sys.exit("Chave 'content' não encontrada no HTML.")
    start = m.end() - 1  # posição do '{'
    braces = 0
    i = start
    while i < len(text):
        if text[i] == '{':
            braces += 1
        elif text[i] == '}':
            braces -= 1
            if braces == 0:
                json_str = text[start:i+1]
                break
        i += 1
    else:
        sys.exit('Não foi possível fechar as chaves do JSON.')
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        sys.exit(f'Erro ao parsear JSON: {e}')
    return data

def main():
    if len(sys.argv) != 3:
        print('Uso: python scripts/extrair_json.py <html_file> <slug>')
        sys.exit(1)
    html_file = Path(sys.argv[1])
    slug = sys.argv[2]
    if not html_file.exists():
        sys.exit(f'Arquivo {html_file} não encontrado')
    data = extract_content(html_file)
    out_path = Path('data')/f'{slug}.yml'
    out_path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    print(f'YAML gerado em {out_path}')

if __name__ == '__main__':
    main()
