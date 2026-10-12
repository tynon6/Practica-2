# Ejercicio 1. Entorno de Desarrollo y Configuración

En este documento se describe la configuración del entorno de desarrollo, la virtualización con Docker y el flujo de trabajo utilizado para la ejecución y validación del proyecto.

---

## 1.1. Configuración de Docker y Contenedores

Para garantizar un entorno de desarrollo reproducible e independiente del sistema operativo anfitrión, la aplicación y las pruebas se ejecutan sobre contenedores Docker.

### Dockerfile
El archivo `Dockerfile` ubicado en la raíz/entorno define la imagen base con **Python 3.10+**, instala las dependencias necesarias descritas en `requirements.txt` (incluyendo `flet` para la interfaz gráfica/web y `pytest` para las pruebas unitarias) y establece las variables de entorno requeridas.

### Docker Compose
A través del archivo `compose.yml` (o `docker-compose.yml`), se gestionan los servicios del contenedor. Permite compilar y levantar el entorno de trabajo mediante comandos simplificados.

**Comandos principales para gestionar el entorno:**
- **Construir la imagen:** `docker compose build`
- **Levantar el contenedor:** `docker compose up -d`
- **Detener el entorno:** `docker compose down`

---

## 1.2. Requisitos y Dependencias (`requirements.txt`)

El proyecto utiliza las siguientes librerías principales de Python:
- **`pytest`**: Framework para la ejecución automatizada de pruebas unitarias sobre los módulos de autómatas.
- **`flet`**: Framework para la construcción de la interfaz gráfica y aplicación web del simulador.

---

## 1.3. Verificación del Entorno y Ejecución de Pruebas

Para verificar que el entorno está correctamente configurado y listo para desarrollo:

1. **Ejecución local o dentro del contenedor:**
   ```bash
   pytest
