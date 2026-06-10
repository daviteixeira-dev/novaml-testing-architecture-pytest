import sys
import os
import pytest
from fastapi.testclient import TestClient

# 1. Força o Python a enxergar a pasta do Lazuli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vendor/novaml-api')))

# 2. Carrega as variáveis do .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../../vendor/novaml-api/.env'))

# Importa o app e a engine de banco de dados do projeto do Lazuli
from src.app import app
from src.db import engine  # Ajuste o nome da importação se a engine estiver em outro arquivo (ex: database.py)
from sqlmodel import SQLModel  # Como a API usa SQLModel, importamos para gerar as tabelas

# 3. Inicializa o cliente de testes
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_banco_de_dados():
    """Garante que todas as tabelas do banco SQL existam antes de rodar qualquer teste"""
    # Cria as tabelas necessárias (como a 'storedmodel') no SQLite local
    SQLModel.metadata.create_all(engine)
    yield
    # Caso queira limpar após os testes, descomente a linha abaixo:
    # SQLModel.metadata.drop_all(engine)

def test_health_check_deve_retornar_200():
    """Verifica se o servidor está online e respondendo na rota raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server up and running!"}

def test_model_types_deve_retornar_lista():
    """Verifica se a rota de tipos de modelo retorna uma lista válida"""
    response = client.get("/model_types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_treino_de_modelo_com_sucesso(tmp_path):
    """Valida se o envio das configurações de treino via JSON funciona com sucesso"""
    
    # 1. Criamos um arquivo CSV real em uma pasta temporária gerenciada pelo Pytest
    pasta_temporaria = tmp_path / "dados"
    pasta_temporaria.mkdir()
    arquivo_csv = pasta_temporaria / "dados_treino.csv"
    
    # Nova massa de dados: Relação matemática linear perfeita para evitar score 'nan'
    dados = (
        "feature1,feature2,target\n"
        "1.0,2.0,2.0\n"
        "2.0,4.0,4.0\n"
        "3.0,6.0,6.0\n"
        "4.0,8.0,8.0\n"
        "5.0,10.0,10.0\n"
        "6.0,12.0,12.0"
    )
    arquivo_csv.write_text(dados)
    
    # 2. Montamos o payload baseado nas regras descobertas
    payload = {
        "model_type": "linear-regression",
        "dataset_file_path": str(arquivo_csv.resolve()),
        "target_name": "target",
        "feature_names": ["feature1", "feature2"]
    }
    
    # 3. Disparamos a requisição POST passando o payload JSON
    response = client.post("/train", json=payload)
    
    # 4. Validações de QA (O FastAPI retorna 201 quando cria um recurso com sucesso)
    assert response.status_code == 201
    assert "message" in response.json() or "id" in response.json()