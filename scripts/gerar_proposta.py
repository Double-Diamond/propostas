#!/usr/bin/env python3
"""
Script para gerar propostas HTML a partir de templates e arquivos JSON.
Este script é uma alternativa ao criar-proposta.sh, usando um template HTML direto
em vez de depender do React para renderização.
"""

import os
import sys
import json
import re
import shutil

def main():
    # Verificar argumentos
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <NOME_ARQUIVO_JSON>")
        print(f"Exemplo: {sys.argv[0]} thiago-pessoa")
        sys.exit(1)

    # Configurações
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    template_dir = os.path.join(base_dir, "templates")
    output_dir = os.path.join(base_dir, "output")
    
    # Garantir que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Obter o nome do arquivo JSON
    client_json_name = sys.argv[1]
    json_file = os.path.join(data_dir, f"{client_json_name}.json")
    
    # Verificar se o arquivo JSON existe
    if not os.path.isfile(json_file):
        print(f"Erro: Arquivo JSON não encontrado: {json_file}")
        print("Disponíveis:")
        for f in os.listdir(data_dir):
            if f.endswith('.json'):
                print(f"  {os.path.splitext(f)[0]}")
        sys.exit(1)
    
    # Carregar os dados do cliente
    with open(json_file, 'r', encoding='utf-8') as f:
        client_data = json.load(f)
    
    # Definir o arquivo de template
    template_file = os.path.join(template_dir, "simples.html")
    
    # Verificar se o arquivo de template existe
    if not os.path.isfile(template_file):
        print(f"Erro: Template não encontrado: {template_file}")
        sys.exit(1)
    
    # Ler o conteúdo do template
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Substituir as variáveis do template
    output_html = replace_variables(template, client_data)
    
    # Nome do arquivo de saída
    client_slug = client_data['cliente']['nome'].lower().replace(' ', '-')
    output_file = os.path.join(output_dir, f"{client_slug}.html")
    
    # Salvar o arquivo HTML de saída
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_html)
    
    print(f"Proposta gerada com sucesso: {output_file}")
    
    # Criar links simbólicos para as imagens
    create_symlinks(base_dir, output_dir, client_slug)
    
    print("\nPara visualizar a proposta, abra o arquivo no navegador:")
    print(f"open {output_file}")


def replace_variables(template, data):
    """
    Substitui as variáveis do template pelos valores correspondentes no JSON.
    Suporta variáveis simples como {{proposta.titulo}} e loops como {{#each secoes.escopo.itens}}
    """
    # Substituir loops {{#each array}}...{{/each}}
    template = process_each_loops(template, data)
    
    # Substituir variáveis simples {{var}}
    pattern = r'\{\{([^#\/][^}]+)\}\}'
    for match in re.finditer(pattern, template):
        var_path = match.group(1).strip()
        value = get_nested_value(data, var_path)
        if value is not None:
            template = template.replace(match.group(0), str(value))
    
    return template


def process_each_loops(template, data):
    """
    Processa os blocos de loop {{#each array}}...{{/each}}
    """
    each_pattern = r'\{\{#each\s+([^}]+)\}\}(.*?)\{\{\/each\}}'
    
    # Continuar processando até não encontrar mais padrões
    while re.search(each_pattern, template, re.DOTALL):
        for match in re.finditer(each_pattern, template, re.DOTALL):
            array_path = match.group(1).strip()
            loop_content = match.group(2)
            
            array_value = get_nested_value(data, array_path)
            if array_value and isinstance(array_value, list):
                replacement = ""
                for item in array_value:
                    item_content = loop_content.replace("{{this}}", str(item))
                    
                    # Se o item for um dicionário, substituir {{key}} por item[key]
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if isinstance(value, str):
                                item_content = item_content.replace(f"{{{{{key}}}}}", value)
                            
                            # Para arrays dentro de objetos nos loops
                            if isinstance(value, list):
                                inner_pattern = f'\\{{{{{key}\\.([^}}]+)\\}}}}'
                                for inner_match in re.finditer(inner_pattern, item_content):
                                    inner_key = inner_match.group(1).strip()
                                    inner_content = process_each_loops(
                                        f'{{{{#each {key}}}}}{inner_content}{{{{/each}}}}', 
                                        {key: value}
                                    )
                                    item_content = item_content.replace(inner_match.group(0), inner_content)
                    
                    replacement += item_content
                
                template = template.replace(match.group(0), replacement)
    
    return template


def get_nested_value(data, path):
    """
    Obtém um valor aninhado em um dicionário usando uma notação de ponto.
    Ex: 'proposta.titulo' retorna data['proposta']['titulo']
    """
    keys = path.split('.')
    value = data
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        print(f"Aviso: Chave '{path}' não encontrada nos dados.")
        return None


def create_symlinks(base_dir, output_dir, client_slug):
    """
    Cria links simbólicos para as imagens necessárias.
    """
    # Lista de arquivos para criar links simbólicos
    symlinks = [
        ("dd_logo_light.png", "../dd_logo_light.png"),
        ("dd_logo_alltype_light.png", "../dd_logo_alltype_light.png"),
        ("hero-image.jpg", "../hero-image.jpg"),
        (f"{client_slug}-logo.png", f"../assets/{client_slug}/logo.png"),
        (f"{client_slug}-logo-white.png", f"../assets/{client_slug}/logo-white.png"),
    ]
    
    # Criar links simbólicos
    for link_name, target in symlinks:
        link_path = os.path.join(output_dir, link_name)
        target_path = os.path.join(base_dir, target.replace("../", ""))
        
        # Remover o link simbólico se já existir
        if os.path.islink(link_path):
            os.unlink(link_path)
        
        # Criar link simbólico apenas se o destino existir
        if os.path.exists(target_path):
            try:
                os.symlink(target, link_path)
            except FileExistsError:
                # Se o arquivo já existe e não é um link simbólico, substituir
                if os.path.exists(link_path):
                    os.remove(link_path)
                os.symlink(target, link_path)
            except Exception as e:
                print(f"Aviso: Não foi possível criar o link simbólico {link_path}: {e}")


if __name__ == "__main__":
    main()
