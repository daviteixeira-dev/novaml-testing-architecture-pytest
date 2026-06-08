# Plano de Testes de Software - Projeto NOVAML
## Em conformidade com a Norma ISO/IEC/IEEE 29119-3

### 1. Introdução e Contexto do Projeto
O NOVAML é uma plataforma No-Code desktop para Machine Learning aplicado à astronomia. Este documento estabelece a estratégia de garantia de qualidade para validar a integração entre a interface (Flutter) e os backends locais em Python (FastAPI e Assistente RAG/Ollama).

### 2. Escopo do Teste (Features Ofertadas)
*   **Em Escopo (A automatizar nesta suíte):**
    *   Validação de disponibilidade de endpoints (`/health`).
    *   Ingestão e análise descritiva de datasets astronômicos (`/upload-csv`).
    *   Inferência e pipelines do assistente conversacional RAG com contexto de CSV (`/chat`).
*   **Fora do Escopo:**
    *   Compilação de executáveis de produção para Windows 11.

### 3. Matriz de Análise de Risco Técnico (Foco Acadêmico)

| Identificador | Risco Mapeado | Impacto | Probabilidade | Estratégia de Mitigação no QA |
| :--- | :--- | :---: | :---: | :--- |
| **R-01** | Sobrecarga de hardware local (RAM/CPU) por leitura de grandes arquivos CSV. | Alto | Alta | Testes de robustez com datasets sintéticos de até 100 mil linhas, monitorando tempo de resposta. |
| **R-02** | Alucinação ou quebra da cadeia RAG com arquivos CSV mal estruturados. | Médio | Alta | Injeção de payloads corrompidos (falta de headers fotométricos do SDSS) e asserção de códigos HTTP 4xx. |
| **R-03** | Instabilidade ou timeout do modelo Ollama (qwen2.5:7b) local. | Alto | Média | Implementação de políticas de timeout explícitas e asserções de tempo limite nas requisições HTTPX. |

### 4. Critérios de Aceite e Conclusão (Quality Gates)
*   **Critério de Entrada:** Código do backend disponível em localhost portas `8000` (API) e `8001` (Chat).
*   **Critério de Saída (Sucesso):** 100% dos testes funcionais críticos e de contrato passando sem erros de regressão. Zero erros do tipo `500 Internal Server Error`.
