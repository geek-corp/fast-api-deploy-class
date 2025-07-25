FROM python:3.11

WORKDIR /app

# Instalar curl para health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY pytest.ini .

# Crear directorios para reportes con permisos correctos
RUN mkdir -p /app/htmlcov && chmod 755 /app/htmlcov

# Crear un usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Configurar variables de entorno para pytest
ENV PYTHONPATH=/app
ENV COVERAGE_FILE=/app/.coverage

# Exponer el puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD ["curl", "-f", "http://localhost:8000/"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]