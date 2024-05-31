
# Proyecto de Ejemplo CrewAI

Este proyecto demuestra el uso de CrewAI para realizar diversas tareas automatizadas utilizando agentes. Contiene tres scripts principales: `escritor.py`, `imagenes.py`, y `newsletter.py`.

## Instalación

Para instalar y ejecutar este proyecto, necesitarás instalar los siguientes paquetes:

```bash
# Instalar el paquete principal de CrewAI
pip install crewai

# Instalar el paquete principal de CrewAI y el paquete de herramientas
pip install 'crewai[tools]'

pip install langchain
pip install pillow
pip install python-dotenv
```

## Archivos del Proyecto

### `escritor.py`

Este script utiliza CrewAI para generar relatos ambientados en la Segunda Guerra Mundial y verificar la precisión histórica de los mismos.

### `imagenes.py`

Este script utiliza CrewAI para generar frases inspiradoras y luego crear imágenes con esas frases.

### `newsletter.py`

Este script utiliza CrewAI para buscar información sobre los proyectos y compañías más emocionantes en el espacio de IA y aprendizaje automático en 2024, crear un informe detallado, escribir una entrada de blog y traducir ambos al español.

## Configuración del Entorno

Para ejecutar `newsletter.py`, necesitas crear un archivo `.env` con la siguiente estructura:

```env
SERP_API_KEY=tu_serp_api_key_aqui
```

## Ejecución de los Scripts

Para ejecutar cualquiera de los scripts, simplemente utiliza el comando `python` seguido del nombre del archivo. Por ejemplo:

```bash
python escritor.py
```

```bash
python imagenes.py
```

```bash
python newsletter.py
```

### Estructura de los Scripts

#### `escritor.py`

- Define agentes para escribir relatos y verificar la precisión histórica.
- Tareas secuenciales: escribir, verificar y editar relatos.

#### `imagenes.py`

- Define un agente para generar frases inspiradoras.
- Utiliza una herramienta para crear imágenes basadas en las frases generadas.

#### `newsletter.py`

- Define agentes para buscar información, escribir blogs y traducir textos.
- Tareas secuenciales: búsqueda de información, redacción de blogs y traducción.

---

Si tienes alguna pregunta o necesitas más información, por favor consulta la [documentación de CrewAI](https://docs.crewai.io) o abre un issue en este repositorio.
