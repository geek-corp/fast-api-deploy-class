import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Cliente de pruebas para FastAPI"""
    return TestClient(app)

@pytest.fixture
def app_instance():
    """Instancia de la aplicación FastAPI"""
    return app 