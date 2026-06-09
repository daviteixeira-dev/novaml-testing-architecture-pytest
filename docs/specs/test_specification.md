# Especificação de Casos de Teste (BDD / Gherkin)

## Mapeamento do Fluxo do Assistente Inteligente (RAG / Ollama)

### Caso de Teste: CT-001 — Upload de Dataset Astronômico e Resumo Automático

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-001 |
| **Título / Objetivo** | Validar o upload com sucesso de dataset SDSS e a geração automática do resumo estatístico. |
| **Pré-condições** | 1. API do assistente de IA (novaml-chat) ativa localmente.<br>2. Endpoint `/upload` operacional. |
| **Cenário Gherkin** | **Dado** que a API do assistente de IA está ativa no ambiente local<br>**Quando** o usuário envia um arquivo `.csv` válido com dados fotométricos do SDSS<br>**Então** o sistema deve retornar o status HTTP 200<br>**E** deve fornecer um `session_id` único no formato UUID<br>**E** o `summary` deve conter as dimensões de linhas e colunas processadas |
| **Passos de Execução** | 1. Preparar uma requisição HTTP POST para o endpoint de upload.<br>2. Anexar o arquivo de massa fotométrica no corpo da requisição (`multipart/form-data`).<br>3. Disparar a requisição e capturar a resposta do servidor. |
| **Dados de Entrada** | Arquivo `sdss_stars_sample.csv` (Contendo colunas obrigatórias como: `ra`, `dec`, `u`, `g`, `r`, `i`, `z`). |
| **Resultado Esperado** | 1. Código de Status HTTP: 200 OK.<br>2. Corpo da resposta contendo um JSON válido.<br>3. Campo `session_id` correspondendo a um padrão Regex UUIDv4.<br>4. Campo `summary` exibindo o texto com o total exato de registros e colunas do arquivo enviado. |
| **Pós-condições** | Sessão de chat criada e ativa na base vetorial temporária (ChromaDB). |
 
### Caso de Teste: CT-002 — Consulta Contextualizada ao Assistente Local (RAG)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-002 |
| **Título / Objetivo** | Validar o tempo de resposta e a precisão do contexto científico retornado pelo modelo Ollama. |
| **Pré-condições** | 1. Execução bem-sucedida do CT-001 com um `session_id` válido e ativo.<br>2. Modelo local Ollama carregado e pronto para inferência. |
| **Cenário Gherkin** | **Dado** que um arquivo `.csv` foi previamente carregado com sucesso obtendo um `session_id`<br>**Quando** o usuário envia uma pergunta técnica contendo o `session_id` ativo<br>**Então** o sistema deve processar a requisição sem estourar o tempo limite de rede<br>**E** a resposta deve conter a chave de dados `answer` preenchida com a justificativa científica do modelo |
| **Passos de Execução** | 1. Montar um payload JSON contendo o `session_id` gerado no CT-001 e a string da pergunta técnica.<br>2. Enviar uma requisição HTTP POST para o endpoint de chat/pergunta.<br>3. Medir o tempo total de resposta da API.<br>4. Validar as chaves do dicionário retornado. |
| **Dados de Entrada** | Payload JSON: `{"session_id": "uuid-obtido-no-ct001", "question": "Explique a distribuição das estrelas identificadas com base no gráfico PCA."}` |
| **Resultado Esperado** | 1. Código de Status HTTP: 200 OK.<br>2. Tempo total da transação inferior ao timeout estipulado (ex: 30 segundos para inferência local).<br>3. Presença da chave `answer` contendo texto científico legível e contextualizado aos dados enviados. |
| **Pós-condições** | O histórico da conversa é atualizado na sessão correspondente. |

## Mapeamento do Núcleo de Processamento de Dados (`CsvDataloader`)

### Caso de Teste: CT-003 — Separação e Particionamento de Dados com Sucesso (Cenário Feliz)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-003 |
| **Título / Objetivo** | Validar se o carregador consegue processar o CSV, isolar as variáveis preditoras/alvo e realizar a divisão de treino/teste na proporção correta. |
| **Pré-condições** | 1. Arquivo CSV estruturado corretamente salvo no diretório temporário ou acessível pela aplicação.<br>2. Formato do arquivo contendo colunas de features numéricas/categóricas e uma coluna alvo demarcada. |
| **Cenário Gherkin** | **Dado** que o arquivo `.csv` astronômico possui colunas de atributos e uma coluna alvo válidas<br>**Quando** o método de particionamento `train_test_split` é acionado com uma proporção de 80/20<br>**Então** o sistema deve segmentar os dados sem gerar exceções estruturais<br>**E** a quantidade de registros resultantes nos conjuntos de treino e teste deve corresponder matematicamente ao percentual solicitado |
| **Passos de Execução** | 1. Instanciar a classe `CsvDataloader` passando o caminho do arquivo válido.<br>2. Invocar o método `load_xy` especificando o nome da coluna alvo (ex: `class`).<br>3. Invocar o método `train_test_split` passando a tupla de dados e o parâmetro `test_size=0.2`.<br>4. Verificar as dimensões das matrizes resultantes (`X_train`, `X_test`, `y_train`, `y_test`). |
| **Dados de Entrada** | Arquivo contendo 1.000 linhas (p. 5). Parâmetros: `target_column="class"`, `feature_columns=["ra", "dec", "u", "g", "r", "i", "z"]`, `test_size=0.2`. |
| **Resultado Esperado** | 1. Execução limpa (sem erros de código).<br>2. Os conjuntos `X_train` e `y_train` devem conter exatamente 800 linhas.<br>3. Os conjuntos `X_test` e `y_test` devem conter exatamente 200 linhas. |
| **Pós-condições** | Os conjuntos de dados segmentados ficam disponíveis em memória na pipeline de ML prontos para o algoritmo de treino. |

### Caso de Teste: CT-004 — Tentativa de Carregamento com Variável Alvo Inexistente (Falha)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-004 |
| **Título / Objetivo** | Garantir que o sistema interrompa o fluxo e lance a exceção adequada se o usuário indicar uma coluna alvo (Target) que não existe no arquivo. |
| **Pré-condições** | 1. Arquivo CSV carregado na aplicação, mas sem a coluna configurada pelo usuário. |
| **Cenário Gherkin** | **Dado** que o arquivo `.csv` astronômico foi carregado no sistema<br>**Quando** o usuário tenta isolar as variáveis informando uma coluna alvo inexistente no arquivo<br>**Então** o sistema deve abortar o processamento imediatamente<br>**E** deve disparar especificamente a exceção `UnexistentTargetError` |
| **Passos de Execução** | 1. Instanciar a classe `CsvDataloader` com o arquivo CSV de teste.<br>2. Invocar o método `load_xy` passando um nome de coluna aleatório ou incorreto.<br>3. Capturar a exceção gerada pela chamada do método. |
| **Dados de Entrada** | Arquivo CSV padrão. Parâmetro: `target_column="coluna_fantasma"`. |
| **Resultado Esperado** | 1. O fluxo de código deve disparar a exceção personalizada `UnexistentTargetError`.<br>2. Nenhuma operação subsequente de particionamento ou treinamento de modelo deve ser executada. |
| **Pós-condições** | O estado do sistema permanece íntegro, impedindo que dados corrompidos ou pipelines inválidas quebrem o backend. |

### Caso de Teste: CT-005 — Tentativa de Carregamento com Atributos Inexistentes (Falha)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-005 |
| **Título / Objetivo** | Garantir o lançamento da exceção correta se alguma das colunas de atributos (Features) selecionadas no painel visual não constar no arquivo físico. |
| **Pré-condições** | 1. Arquivo CSV carregado na aplicação. |
| **Cenário Gherkin** | **Dado** que o arquivo `.csv` astronômico foi carregado no sistema<br>**Quando** o método de extração de variáveis tenta buscar colunas de atributos especificadas que não constam no arquivo físico<br>**Então** o sistema deve capturar a inconsistência estrutural<br>**E** deve disparar especificamente a exceção `UnexistentFeatureError` |
| **Passos de Execução** | 1. Instanciar a classe `CsvDataloader` com o arquivo CSV de teste.<br>2. Invocar o método `load_xy` ou `load_x` contendo na lista de atributos algum nome grafado incorretamente (ex: `infrared_band` em vez de `z`).<br>3. Capturar a exceção gerada. |
| **Dados de Entrada** | Arquivo CSV padrão. Parâmetro: `feature_columns=["ra", "dec", "u", "coluna_errada_que_nao_existe"]`. |
| **Resultado Esperado** | 1. O sistema dispara com sucesso a exceção customizada `UnexistentFeatureError`.<br>2. O carregador bloqueia o envio da matriz nula para os algoritmos de Machine Learning. |
| **Pós-condições** | O backend barra a operação e retorna o erro mapeado, permitindo que a interface gráfica trate o aviso ao usuário. |

## Mapeamento do Fluxo de Treinamento No-Code, Persistência e Exportação

### Caso de Teste: CT-006 — Treinamento Automatizado de Modelo e Geração de Métricas (Cenário Feliz)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-006 |
| **Título / Objetivo** | Validar se o motor executa o treinamento do classificador astronômico com sucesso e retorna as métricas de avaliação regulamentares. |
| **Pré-condições** | 1. Dados previamente fatiados pelo `CsvDataloader` (`X_train`, `y_train`) disponíveis em memória.<br>2. Algoritmo selecionado configurado com hiperparâmetros válidos. |
| **Cenário Gherkin** | **Dado** que os conjuntos de treino de dados astronômicos estão carregados e normalizados<br>**Quando** o usuário dispara a requisição de treinamento definindo um algoritmo e seus hiperparâmetros<br>**Então** o sistema deve processar o ajuste do classificador sem falhas de *runtime*<br>**E** deve retornar um payload contendo métricas de desempenho populadas (Acurácia, F1-Score) |
| **Passos de Execução** | 1. Instanciar a classe `AutomatedTrainer` ou efetuar um POST no endpoint `/train`.<br>2. Passar a matriz de treino e as configurações de hiperparâmetros no payload.<br>3. Chamar o método `.fit()` do modelo interno correspondente.<br>4. Capturar o retorno do dicionário contendo o relatório de classificação. |
| **Dados de Entrada** | JSON de Configuração: `{"model_type": "RandomForest", "hyperparameters": {"n_estimators": 100, "max_depth": 10}}`. |
| **Resultado Esperado** | 1. O código de status retornado deve ser HTTP 200 OK.<br>2. O payload JSON de resposta deve conter as chaves `accuracy`, `precision`, `recall` e `f1_score`.<br>3. Todos os valores de métricas devem ser numéricos (*Float*) contidos no intervalo realista entre 0.0 e 1.0. |
| **Pós-condições** | O objeto do modelo treinado fica retido temporariamente na memória RAM do servidor para as etapas de persistência e download. |

### Caso de Teste: CT-007 — Persistência e Exportação do Modelo Treinado (Artefato .pkl e SQLite)

| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-007 |
| **Título / Objetivo** | Validar se o sistema serializa o modelo adequadamente através da biblioteca Pickle e se registra com sucesso o histórico da execução na tabela do banco SQLite. |
| **Pré-condições** | 1. Execução bem-sucedida do CT-006 (Modelo treinado ativo em memória).<br>2. Conexão com o banco de dados SQLite (`nova_ml.db`) ativa e permissões de escrita concedidas no diretório de artefatos. |
| **Cenário Gherkin** | **Dado** que o modelo de Machine Learning concluiu o seu treinamento com sucesso<br>**Quando** o comando de finalização e salvamento do experimento é acionado pelo pipeline<br>**Então** o sistema deve gerar e salvar um arquivo binário `.pkl` válido no disco local<br>**E** deve inserir um novo registro com o ID do modelo, métricas e data/hora na tabela histórica do SQLite |
| **Passos de Execução** | 1. Chamar o método interno de salvamento ou disparar o endpoint correspondente à exportação do modelo.<br>2. Verificar a criação física do arquivo binário na pasta de outputs do projeto.<br>3. Abrir uma conexão de leitura paralela com o banco SQLite e executar uma query de seleção (`SELECT`) na tabela de modelos. |
| **Dados de Entrada** | Comando de salvamento acionado com os parâmetros: `model_id="run_sdss_rf_001"`, `directory="./models/exports/"`. |
| **Resultado Esperado** | 1. Um arquivo chamado `run_sdss_rf_001.pkl` deve ser gravado no diretório alvo e possuir tamanho maior que 0 KB.<br>2. A tabela do SQLite deve conter exatamente uma nova linha correspondente, com as colunas preenchidas corretamente (`id`, `model_type`, `accuracy`, `timestamp`). |
| **Pós-condições** | O modelo está registrado permanentemente, permitindo que a interface web liste o histórico de execuções passadas no painel. |

### Caso de Teste: CT-008 — Execução de Predições (Módulo Predict / Inferência)


| Campo | Descrição Detalhada |
| :--- | :--- |
| **ID do Caso de Teste** | CT-008 |
| **Título / Objetivo** | Validar se um arquivo de modelo anteriormente exportado consegue carregar na memória e classificar novos registros astronômicos com sucesso. |
| **Pré-condições** | 1. Arquivo binário `.pkl` de um modelo válido gerado previamente e acessível em disco.<br>2. Massa de teste (`X_test`) sem rótulo de classe carregada. |
| **Cenário Gherkin** | **Dado** que um arquivo binário `.pkl` correspondente a um modelo válido está disponível no servidor<br>**Quando** uma matriz de novas *features* é enviada ao endpoint de predição junto ao ID do modelo<br>**Então** o sistema deve desserializar o arquivo e realizar a inferência matemática<br>**E** deve retornar uma lista de predições contendo os rótulos preditos para cada entrada fornecida |
| **Passos de Execução** | 1. Realizar uma requisição HTTP POST para o endpoint `/predict`.<br>2. Passar no payload o identificador do modelo gravado e a matriz de dados contendo os dados fotométricos de teste.<br>3. Analisar o vetor de resposta. |
| **Dados de Entrada** | JSON contendo: `{"model_id": "run_sdss_rf_001", "data": [[21.34, 19.22, 18.54, 18.11, 17.90]]}`. |
| **Resultado Esperado** | 1. Retorno com código HTTP 200 OK.<br>2. O corpo da resposta JSON deve conter o campo `predictions`.<br>3. O conteúdo de `predictions` deve ser um *array* com a classificação predita pelo modelo (ex: `["STAR"]` ou `["GALAXY"]`). |
| **Pós-condições** | O arquivo do modelo é fechado em memória e o resultado é devolvido íntegro para o cliente HTTP. |

