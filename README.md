# Flask CRUD Demo

Proyecto de referencia que implementa un CRUD completo para Clientes y Transacciones con Flask 3, SQLAlchemy 2 y PostgreSQL. Incluye documentación OpenAPI, pruebas automatizadas, configuración de CI/CD y soporte listo para SonarQube.

## Características principales

- API REST versionada en `/api/v1` con Flask-RESTX y documentación Swagger.
- Modelos `Client` y `Transaction` con relaciones 1-N y eliminación en cascada de transacciones al borrar un cliente.
- Validación de payloads con Marshmallow y manejo consistente de errores HTTP 400/404/409.
- Servicios organizados por capas (models, schemas, services, resources).
- Pruebas unitarias y de integración con `pytest` y reportes de cobertura (`coverage.xml`).
- Linter/formatter con `ruff`, `black` e `isort` integrados mediante pre-commit.
- Dockerfile y docker-compose con PostgreSQL 15.
- Workflow de GitHub Actions que ejecuta lint, pruebas y carga el reporte de cobertura. Job opcional para SonarQube.
- Configuración de `sonar-project.properties` lista para análisis estático.

## Requisitos previos

- Python 3.11+
- Docker y docker-compose (opcional para despliegue contenedorizado)

## Instalación local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
flask --app app:create_app run
```

La API estará disponible en `http://localhost:5000/api/v1` y la documentación interactiva en `http://localhost:5000/api/v1/docs`.

## Uso con Docker

```bash
make docker-up
```

Esto construye los contenedores para la aplicación (`web`) y la base de datos PostgreSQL (`db`). Una vez levantados, accede a la documentación Swagger en `http://localhost:5000/api/v1/docs`.

Para detener y limpiar los contenedores:

```bash
make docker-down
```

## Migraciones de base de datos

Se utiliza Flask-Migrate (Alembic). Para crear nuevas migraciones:

```bash
flask --app app:create_app db migrate -m "Descripcion de la migracion"
flask --app app:create_app db upgrade
```

## Ejecución de pruebas y cobertura

```bash
make test
make coverage  # genera coverage.xml
```

Los resultados se almacenan en `coverage.xml`, listo para su consumo por SonarQube u otras herramientas.

## Pre-commit

Instala los hooks de pre-commit después de instalar dependencias:

```bash
pre-commit install
```

## SonarQube

El análisis está configurado mediante `sonar-project.properties`. Para ejecutarlo localmente:

```bash
sonar-scanner \
  -Dsonar.projectKey=flask-crud-demo \
  -Dsonar.sources=app \
  -Dsonar.tests=tests \
  -Dsonar.python.coverage.reportPaths=coverage.xml
```

En CI, establece las variables `SONAR_HOST_URL` y `SONAR_TOKEN` (ya sea como Secrets o Vars) para habilitar el job opcional `sonar`.

## Estructura del proyecto

```
flask-crud-demo/
├─ app/
│  ├─ config.py
│  ├─ extensions.py
│  ├─ models/
│  ├─ schemas/
│  ├─ services/
│  └─ resources/
├─ migrations/
├─ tests/
├─ docker-compose.yml
├─ Dockerfile
├─ pyproject.toml
├─ sonar-project.properties
├─ .github/workflows/ci.yml
├─ .pre-commit-config.yaml
└─ Makefile
```

## Decisiones de diseño

- **Eliminación en cascada:** La relación `Client -> Transaction` utiliza `cascade="all, delete-orphan"` y `ForeignKey(..., ondelete="CASCADE")`. Se eligió eliminar las transacciones asociadas cuando se borra un cliente para mantener la consistencia y evitar registros huérfanos.
- **Validaciones:** Marshmallow controla el formato de entrada (emails válidos, montos positivos, enumeraciones) y el servicio agrega validaciones de reglas de negocio (unicidad de email, existencia del cliente).
- **Pagos y filtros:** La paginación y filtros básicos se aplican en la capa de servicio para facilitar su reutilización en otros contextos.
- **Aplicación factory:** Permite crear instancias específicas por entorno (desarrollo, pruebas, producción) y facilita la ejecución de pruebas aisladas.

## Endpoints principales

- `POST /api/v1/clients`
- `GET /api/v1/clients`
- `GET /api/v1/clients/{id}`
- `PUT /api/v1/clients/{id}`
- `DELETE /api/v1/clients/{id}`
- `GET /api/v1/clients/{id}/transactions`
- `POST /api/v1/transactions`
- `GET /api/v1/transactions`
- `GET /api/v1/transactions/{id}`
- `PUT /api/v1/transactions/{id}`
- `DELETE /api/v1/transactions/{id}`
- `GET /health`

