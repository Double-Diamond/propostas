#!/bin/bash

# Script para criar propostas a partir de arquivos JSON de conteúdo

# Verifica argumentos
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <NOME_ARQUIVO_JSON>"
    echo "Exemplo: $0 thiago-pessoa"
    exit 1
fi

# Configurações
DATA_DIR="./data"
TEMPLATE_DIR="./templates"
OUTPUT_DIR="./output"
ASSETS_DIR="./assets"
BASE_TEMPLATE="${TEMPLATE_DIR}/base.html"
JSON_FILE="${DATA_DIR}/${1}.json"

# Verifica se o arquivo JSON existe
if [ ! -f "$JSON_FILE" ]; then
    echo "Erro: Arquivo JSON não encontrado: $JSON_FILE"
    echo "Disponíveis:"
    ls -1 ${DATA_DIR}/*.json | sed "s|${DATA_DIR}/||" | sed 's/\.json$//'
    exit 1
fi

# Extrai informações do JSON usando jq (assumindo que jq está instalado)
if ! command -v jq &> /dev/null; then
    echo "Erro: jq não está instalado. Por favor, instale com 'brew install jq'"
    exit 1
fi

# Extrai dados do cliente
CLIENT_ID=$(jq -r '.cliente.id' $JSON_FILE)
CLIENT_NAME=$(jq -r '.cliente.nome' $JSON_FILE)
CLIENT_SPACE_ID=$(jq -r '.cliente.spaceId' $JSON_FILE)

# Nome do arquivo de saída
CLIENT_SLUG=$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
OUTPUT_FILE="${OUTPUT_DIR}/${CLIENT_SLUG}.html"

# Criar conteúdo JSON para injetar no arquivo HTML
# Isso vai transformar o arquivo JSON do cliente em um formato que pode ser
# injetado diretamente no campo content do __manus_space_editor_info
CONTENT_JSON=$(jq -c '.' $JSON_FILE)

# Cria diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

# Cria uma cópia do template
cp "$BASE_TEMPLATE" "$OUTPUT_FILE"

# Substitui os placeholders básicos
sed -i '' "s/CLIENT_ID/$CLIENT_ID/g" "$OUTPUT_FILE"
sed -i '' "s/CLIENT_NAME/$CLIENT_NAME/g" "$OUTPUT_FILE"
sed -i '' "s/CLIENT_SPACE_ID/$CLIENT_SPACE_ID/g" "$OUTPUT_FILE"

# Substitui o objeto content vazio pelo conteúdo do JSON
# Isso é um pouco mais complexo e requer uma expressão sed mais elaborada
# A linha abaixo encontra a linha com "content: {}" e substitui por "content: {...JSON...}"
sed -i '' "s/content: {},/content: $CONTENT_JSON,/g" "$OUTPUT_FILE"

# Certifica-se de que os caminhos de recursos são relativos (para funcionar em servidor local)
sed -i '' "s|href=\"/|href=\"../|g" "$OUTPUT_FILE"
sed -i '' "s|src=\"/|src=\"../|g" "$OUTPUT_FILE"

# Cria links simbólicos para as imagens na pasta output para facilitar o acesso local
ln -sf ../dd_logo_light.png ${OUTPUT_DIR}/dd_logo_light.png
ln -sf ../dd_logo_alltype_light.png ${OUTPUT_DIR}/dd_logo_alltype_light.png
ln -sf ../hero-image.jpg ${OUTPUT_DIR}/hero-image.jpg
ln -sf ../assets/${CLIENT_SLUG}/logo.png ${OUTPUT_DIR}/${CLIENT_SLUG}-logo.png
ln -sf ../assets/${CLIENT_SLUG}/logo-white.png ${OUTPUT_DIR}/${CLIENT_SLUG}-logo-white.png

echo "Proposta criada com sucesso: $OUTPUT_FILE"
echo ""
echo "Para visualizar a proposta, abra o arquivo no navegador:"
echo "open $OUTPUT_FILE"

# Pergunta se deseja copiar arquivos de logo
echo ""
echo "Deseja criar os arquivos de logo para o cliente? (s/n)"
read CRIAR_LOGOS

if [ "$CRIAR_LOGOS" = "s" ] || [ "$CRIAR_LOGOS" = "S" ]; then
    # Cria diretório para os assets do cliente se não existir
    CLIENT_ASSETS_DIR="${ASSETS_DIR}/${CLIENT_SLUG}"
    mkdir -p "$CLIENT_ASSETS_DIR"
    
    # Copia os logos
    if [ -f "${ASSETS_DIR}/logo.png" ]; then
        cp "${ASSETS_DIR}/logo.png" "${CLIENT_ASSETS_DIR}/logo.png"
    fi
    
    if [ -f "${ASSETS_DIR}/logo-white.png" ]; then
        cp "${ASSETS_DIR}/logo-white.png" "${CLIENT_ASSETS_DIR}/logo-white.png"
    fi
    
    echo "Arquivos de logo criados em: $CLIENT_ASSETS_DIR"
    echo "Não esqueça de substituir esses arquivos pelos logos reais do cliente!"
fi
