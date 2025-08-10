#!/bin/bash

# Script para testar a geração de uma proposta de exemplo

# Verificar se jq está instalado
if ! command -v jq &> /dev/null; then
    echo "Aviso: jq não está instalado. Algumas funcionalidades podem não funcionar corretamente."
    echo "Instale com: brew install jq"
fi

# Definir diretório do projeto
PROJECT_DIR="/Users/robertopeluzzo/Desktop/Projects/propostas"

# Ir para o diretório do projeto
cd "$PROJECT_DIR"

# Gerar uma proposta de exemplo
echo "Gerando proposta de exemplo para Thiago Pessoa..."
./scripts/criar-proposta.sh thiago-pessoa

echo ""
echo "Demonstração concluída!"
echo ""
echo "Estrutura do projeto agora está organizada assim:"
echo ""
echo "propostas/"
echo "├── assets/            # Arquivos de imagem, logos etc."
echo "├── data/              # Arquivos JSON com dados dos clientes"
echo "│   ├── template.json  # Template JSON para novos clientes"
echo "│   └── thiago-pessoa.json # Dados do cliente Thiago Pessoa"
echo "├── output/            # Propostas HTML geradas"
echo "│   └── thiago-pessoa.html # Proposta gerada"
echo "├── scripts/           # Scripts para geração de propostas"
echo "│   └── criar-proposta.sh"
echo "├── static/            # Arquivos CSS, JavaScript e outros recursos"
echo "├── templates/         # Templates HTML base"
echo "│   └── base.html      # Template HTML base"
echo "└── README.md          # Este arquivo"
echo ""
echo "Para criar uma nova proposta:"
echo "1. Copie data/template.json para data/novo-cliente.json"
echo "2. Edite o arquivo JSON com os dados do cliente"
echo "3. Execute: ./scripts/criar-proposta.sh novo-cliente"
