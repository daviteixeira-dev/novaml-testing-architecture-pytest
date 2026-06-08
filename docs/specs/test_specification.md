# Especificação de Casos de Teste (BDD / Gherkin)

## Funcionalidade: Validação do Fluxo RAG com Contexto Astronômico

- Cenário: Upload bem-sucedido de dataset SDSS e resumo automático
    - Dado que a API do assistente de IA está ativa no ambiente local
    - Quando o usuário envia um arquivo ".csv" válido com dados fotométricos do SDSS
    - Então o sistema deve retornar o status HTTP 200
    - E deve fornecer um "session_id" único no formato UUID
    - E o "summary" deve conter as dimensões de linhas e colunas processadas

- Cenário: Análise de comportamento e contexto do Assistente de IA
    - Dado que um arquivo ".csv" foi previamente carregado com sucesso obtendo um "session_id"
    - Quando o usuário envia uma pergunta técnica contendo o "session_id" ativo
    - Então o sistema deve processar a requisição sem estourar o tempo limite de rede
    - E a resposta deve conter a chave de dados "answer" preenchida com a justificativa científica do modelo
