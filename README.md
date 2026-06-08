# 🔬 NOVAML Testing Architecture (PyTest)

Este repositório apresenta uma **arquitetura de testes automatizados de backend e inteligência artificial robusta**, projetada para o ecossistema **NOVAML (No-Code Visual Astronomical Machine Learning)**. O projeto implementa técnicas avançadas de testes de contrato e integração para validar o pipeline RAG (Retrieval-Augmented Generation), motores de Machine Learning locais e ingestão de dados astronômicos, seguindo rigor metodológico acadêmico de P&D.

## 🏗️ Estrutura e Práticas de Arquitetura

O ecossistema utiliza separação rígida de responsabilidades:

- **docs/specs/**: Plano de Testes (ISO/IEC/IEEE 29119-3) e cenários BDD/Gherkin.
- **tests/api/**: Validação do motor backend (`novaml-api`) e pipelines de ML.
- **tests/chat_ia/**: Validação do fluxo do assistente (`novaml-chat`) e ChromaDB/Ollama.
- **tests/utils/**: Geração de massa de dados sintética com Pandas.

## 🛠️ Stack Tecnológica e Requisitos (Windows)

- **Sistema Operacional:** Windows 10 / Windows 11.
- **Linguagem Base:** Python 3.10+.
- **Engine de Testes:** PyTest.
- **Client HTTP:** HTTPX (async).
- **Gerenciador de Dados:** Pandas.

## 🚀 Guia de Configuração Rápida (Windows)

```bash
# Clone e entre na pasta
git clone <url-do-repositorio>
cd novaml-testing-architecture-pytest

# Crie e ative o ambiente virtual (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt

# Executar testes
pytest --html=reports/dashboard_report.html --self-contained-html
```

## 📑 Artefatos e Rigor Acadêmico
Documentos formais na pasta `/docs` detalham o Plano de Testes (ISO 29119-3) e as Especificações de Casos de Teste (BDD), focando em gestão de riscos técnicos e qualidade da infraestrutura local.
