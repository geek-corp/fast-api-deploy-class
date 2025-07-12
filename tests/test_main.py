import pytest
import time

class TestEndpoints:
    """Pruebas para los endpoints de la aplicación FastAPI"""
    
    def test_leer_root(self, client):
        """Prueba el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"mensaje": "¡Hola mundo desde FastAPI!"}
    
    def test_leer_root_response_headers(self, client):
        """Prueba que los headers de respuesta sean correctos"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_leer_root_response_structure(self, client):
        """Prueba la estructura de la respuesta"""
        response = client.get("/")
        json_response = response.json()
        assert "mensaje" in json_response
        assert isinstance(json_response["mensaje"], str)
        assert len(json_response["mensaje"]) > 0

class TestApplicationStructure:
    """Pruebas para la estructura de la aplicación"""
    
    def test_app_instance(self, app_instance):
        """Prueba que la instancia de app esté correctamente configurada"""
        assert app_instance is not None
        assert hasattr(app_instance, "router")
    
    def test_openapi_schema(self, client):
        """Prueba que el schema OpenAPI se genere correctamente"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()
    
    def test_docs_endpoint(self, client):
        """Prueba que el endpoint de documentación funcione"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

class TestErrorHandling:
    """Pruebas para manejo de errores"""
    
    def test_not_found_endpoint(self, client):
        """Prueba que endpoints no existentes devuelvan 404"""
        response = client.get("/endpoint-inexistente")
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}
    
    def test_method_not_allowed(self, client):
        """Prueba que métodos no permitidos devuelvan 405"""
        response = client.post("/")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

class TestPerformance:
    """Pruebas básicas de rendimiento"""
    
    def test_response_time(self, client):
        """Prueba que el tiempo de respuesta sea razonable"""
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # Debería responder en menos de 1 segundo
        assert response.status_code == 200

    def test_multiple_requests(self, client):
        """Prueba múltiples requests consecutivos"""
        responses = []
        for _ in range(5):
            response = client.get("/")
            responses.append(response)
        
        # Todas las respuestas deben ser exitosas
        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"mensaje": "¡Hola mundo desde FastAPI!"}

class TestHealthCheck:
    """Pruebas para verificar el estado de salud de la aplicación"""
    
    def test_app_health(self, client):
        """Prueba básica de salud de la aplicación"""
        response = client.get("/")
        assert response.status_code == 200
        # Verificar que la aplicación responda consistentemente
        response2 = client.get("/")
        assert response.json() == response2.json()

@pytest.mark.parametrize("path", ["/", "/docs", "/openapi.json"])
def test_common_endpoints_accessibility(client, path):
    """Prueba que los endpoints comunes sean accesibles"""
    response = client.get(path)
    # Todos estos endpoints deberían ser accesibles (no 404)
    assert response.status_code != 404 