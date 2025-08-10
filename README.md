# Sistema de Propostas - Double Diamond

Este repositório contém o sistema de propostas da Double Diamond, permitindo a criação de novas propostas para diferentes clientes a partir de templates HTML e arquivos JSON de conteúdo.

## Estrutura do Projeto

```
propostas/
├── assets/            # Arquivos de imagem, logos etc.
├── data/              # Arquivos JSON com dados dos clientes
│   ├── template.json  # Template JSON para novos clientes
│   └── *.json         # Dados específicos de cada cliente
├── output/            # Propostas HTML geradas
├── scripts/           # Scripts para geração de propostas
│   └── criar-proposta.sh
├── static/            # Arquivos CSS, JavaScript e outros recursos
├── templates/         # Templates HTML base
│   └── base.html      # Template HTML base
└── README.md          # Este arquivo
```

## Como Criar uma Nova Proposta

### Passo 1: Criar o arquivo JSON com os dados do cliente

1. Copie o arquivo `data/template.json` para um novo arquivo com o nome do cliente (ex: `data/novo-cliente.json`)
2. Edite o arquivo JSON com os dados específicos do cliente:
   - ID do cliente
   - Nome do cliente
   - ID do espaço no sistema Manus (se aplicável)
   - Conteúdo das seções (escopo, cronograma, investimento, etc.)

### Passo 2: Executar o script de geração da proposta

```bash
cd /caminho/para/propostas
./scripts/criar-proposta.sh nome-do-arquivo-json
```

Exemplo:
```bash
./scripts/criar-proposta.sh thiago-pessoa
```

O script irá:
1. Ler os dados do arquivo JSON
2. Criar um novo arquivo HTML na pasta `output/`
3. Substituir os placeholders com os dados do cliente
4. Oferecer a opção de criar cópias dos arquivos de logo

### Passo 3: Personalizar os logos (opcional)

Se você optar por criar os arquivos de logo no passo anterior:
1. Navegue até a pasta `assets/nome-do-cliente/`
2. Substitua os arquivos de logo pelos logos reais do cliente

## Estrutura do Arquivo JSON

O arquivo JSON contém todas as informações necessárias para personalizar a proposta:

```json
{
  "cliente": {
    "id": "ID_DO_CLIENTE",
    "nome": "NOME_DO_CLIENTE",
    "spaceId": "ID_DO_ESPACO"
  },
  "proposta": {
    "titulo": "Título da Proposta",
    "intro": "Texto introdutório..."
  },
  "secoes": {
    "sobre": {
      "titulo": "Sobre a Double Diamond",
      "conteudo": "Descrição da empresa..."
    },
    "escopo": {
      "titulo": "Escopo do Projeto",
      "conteudo": "Descrição do escopo...",
      "itens": [
        "Item 1",
        "Item 2",
        "..."
      ]
    },
    // Outras seções...
  },
  "contato": {
    "email": "contato@exemplo.com",
    "telefone": "Telefone",
    "site": "site.com"
  }
}
```

## Requisitos

- macOS com shell bash ou zsh
- [jq](https://stedolan.github.io/jq/) instalado (para processamento JSON)
  - Instale com: `brew install jq`

## Contato

Para mais informações, entre em contato com a equipe da Double Diamond.
