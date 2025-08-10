#!/bin/bash

# Script mais simples para modificar diretamente o HTML da proposta

# Verifica argumentos
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <NOME_CLIENTE>"
    echo "Exemplo: $0 thiago-pessoa"
    exit 1
fi

# Configurações
CLIENT_NAME=$1
DATA_DIR="./data"
OUTPUT_DIR="./output"
JSON_FILE="${DATA_DIR}/${CLIENT_NAME}.json"
HTML_FILE="${OUTPUT_DIR}/${CLIENT_NAME}.html"
TEMP_FILE="/tmp/proposta_temp.html"

# Verifica se os arquivos existem
if [ ! -f "$JSON_FILE" ]; then
    echo "Erro: Arquivo JSON não encontrado: $JSON_FILE"
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Erro: Arquivo HTML não encontrado: $HTML_FILE"
    exit 1
fi

# Extrai o título e a introdução do JSON
PROPOSAL_TITLE=$(jq -r '.proposta.titulo' $JSON_FILE)
PROPOSAL_INTRO=$(jq -r '.proposta.intro' $JSON_FILE)

# Adicionar o script como um arquivo separado
cat > "${OUTPUT_DIR}/substituicao.js" << EOF
// Script para garantir que o título e a introdução sejam substituídos
window.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    // Encontrar o elemento h1 com "Transformação Digital" e substituir
    var h1Elements = document.querySelectorAll("h1");
    for (var i = 0; i < h1Elements.length; i++) {
      if (h1Elements[i].textContent.includes("Transformação Digital para")) {
        console.log("Substituindo o título...");
        // Preserva o span com gradient-text se existir
        var spanElement = h1Elements[i].querySelector(".gradient-text");
        if (spanElement) {
          var clientName = spanElement.textContent;
          h1Elements[i].innerHTML = "${PROPOSAL_TITLE} <span class=\"gradient-text\">" + clientName + "</span>";
        } else {
          h1Elements[i].textContent = "${PROPOSAL_TITLE}";
        }
      }
    }
    
    // Substituir a introdução
    var introElements = document.querySelectorAll("p");
    for (var j = 0; j < introElements.length; j++) {
      if (introElements[j].textContent.includes("Uma proposta personalizada de automação") || 
          introElements[j].textContent.includes("elevar a experiência dos seus clientes")) {
        console.log("Substituindo a introdução...");
        introElements[j].textContent = "${PROPOSAL_INTRO}";
      }
    }
  }, 500); // Aguardar 500ms para o React renderizar
});
EOF

# Adicionar referência ao script no HTML
awk 'BEGIN{found=0} /<\/head>/{if(!found){print "  <script src=\"substituicao.js\"></script>"; found=1}} {print}' "$HTML_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$HTML_FILE"

echo "Script de substituição adicionado com sucesso a $HTML_FILE"
echo "Abra o arquivo no navegador para ver as alterações:"
echo "open $HTML_FILE"
