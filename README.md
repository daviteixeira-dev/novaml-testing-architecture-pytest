# 🔬 NOVAML Testing Architecture (PyTest)

Este repositório apresenta uma **arquitetura de testes automatizados de backend e inteligência artificial robusta**, projetada para o ecossistema **NOVAML (No-Code Visual Astronomical Machine Learning)**. O projeto implementa técnicas avançadas de testes de contrato e integração para validar o pipeline RAG (Retrieval-Augmented Generation), motores de Machine Learning locais e ingestão de dados astronômicos, seguindo rigor metodológico acadêmico de P&D.

Para evitar a duplicidade de código e garantir a independência e isolamento do ecossistema de QA, adotamos a estratégia de **Git Submodules**, trazendo os projetos originais de desenvolvimento como dependências acopladas na pasta `vendor/`.

## 🏗️ Estrutura e Práticas de Arquitetura

O ecossistema utiliza separação rígida de responsabilidades e centralização de testes:

- **docs/specs/**: Plano de Testes (ISO/IEC/IEEE 29119-3) e cenários BDD/Gherkin.
- **tests/api/**: Validação do motor backend (`novaml-api`) e pipelines de ML.
- **tests/chat_ia/**: Validação do fluxo do assistente (`novaml-chat`) e ChromaDB/Ollama.
- **tests/utils/**: Geração de massa de dados sintética com Pandas.
- **`vendor/`**: Projetos originais do time de desenvolvimento (API, Chat e App) gerenciados como submódulos vivos.

```text
novaml-testing-architecture-pytest/
├── .gitmodules             # Mapeamento dos submódulos do ecossistema
├── .venv/                  # Ambiente virtual unificado de QA
├── docs/                   # Artefatos e rigor acadêmico
├── tests/                  # Códigos de teste automatizados
└── vendor/                 # Código de produção do time de desenvolvimento
    └── novaml-api/         # Submódulo da API do Lazuli (FastAPI)
```

## 🛠️ Stack Tecnológica e Requisitos (Windows)

- **Sistema Operacional:** Windows 10 / Windows 11.
- **Linguagem Base:** Python 3.10+.
- **Engine de Testes:** PyTest.
- **Client HTTP / Simulação:** HTTPX (async) e FastAPI TestClient.
- **Gerenciador de Dados:** Pandas.

## 🚀 Guia de Configuração Rápida (Windows)

Siga os passos abaixo para configurar o hub de testes unificado na sua máquina:

### 1. Clonar o Repositório com os Submódulos
Como este projeto depende de repositórios externos, use o comando `--recursive` para baixar o projeto de testes e os códigos de produção juntos:
```powershell
git clone --recursive <url-do-repositorio>
cd novaml-testing-architecture-pytest
```
*(Caso já tenha clonado de forma simples, inicialize os submódulos manualmente com: `git submodule update --init --recursive`)*

### 2. Configurar o Ambiente Virtual (.venv)
Crie e ative a `.venv` unificada na raiz do projeto para gerenciar todas as ferramentas de QA:
```powershell
# Criar o ambiente
python -m venv .venv

# Ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Para desativar o ambiente virtual e voltar para o terminal global do seu Windows:
deactivate
```

### 3. Instalar as Dependências
Instale as bibliotecas necessárias para rodar os motores de desenvolvimento do time e as suas ferramentas de teste:
```powershell
# Dependências do motor de produção (Ex: API do Lazuli)
pip install -r vendor/novaml-api/requirements.txt

# Ferramentas de QA do Repositório
pip install pytest httpx python-dotenv sqlmodel
```

### 4. Executar os Testes Automatizados
Para rodar toda a suíte de testes de integração com relatórios detalhados:
```powershell
pytest -v --html=reports/dashboard_report.html --self-contained-html
```

---

## 🧠 Gestão de Dependências: Git Submodules

### O que é e por que usamos?
O **Git Submodule** permite manter repositórios Git externos dentro deste repositório de QA. Ele funciona como um ponteiro para o commit exato do projeto dos desenvolvedores, trazendo dois grandes benefícios de Engenharia de Software:
1. **Isolamento de Escopo:** O código de produção (API/Chat) não se mistura com o código de teste (QA).
2. **Sincronização Dinâmica:** Sempre que o time atualizar as aplicações deles, atualizamos nossa pasta `vendor/` local sem a necessidade de novos clones através do comando:
   ```powershell
   git submodule update --remote --merge
   ```

---

## 📑 Artefatos e Rigor Acadêmico
Documentos formais na pasta `/docs` detalham o Plano de Testes (ISO 29119-3) e as Especificações de Casos de Teste (BDD), focando em gestão de riscos técnicos e qualidade da infraestrutura local.
