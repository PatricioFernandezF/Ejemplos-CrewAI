from dotenv import load_dotenv
import os

from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Process, Crew
from langchain_community.utilities import GoogleSerperAPIWrapper

# Cargar el archivo .env
load_dotenv()

# Acceder a las variables de entorno
SERP_API_KEY = os.getenv('SERP_API_KEY')
os.environ["SERPER_API_KEY"] = SERP_API_KEY

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

llm = ChatOpenAI(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

busqueda = GoogleSerperAPIWrapper()

herramienta_busqueda = Tool(
    name="Buscar en Google",
    func=busqueda.run,
    description="Utilidad para buscar en google",
    llm=llm,
)

explorador = Agent(
    role="Investigador Senior",
    goal="ES MUY IMPORTANTE: No hacer mas de 3 busquedas. Encontrar y explorar los proyectos y compañías más emocionantes en el espacio de IA y aprendizaje automático en 2024",
    backstory="""Eres un estratega experto que sabe cómo identificar tendencias emergentes y compañías en IA, tecnología y aprendizaje automático. 
    Eres excelente encontrando proyectos interesantes en el subreddit LocalLLama. Transformaste datos recopilados en informes detallados con nombres
    de los proyectos y compañías más emocionantes en el mundo de IA/ML. SOLO usa datos recopilados de internet para el informe.
    """,
    verbose=True,
    allow_delegation=False,
    tools=[herramienta_busqueda],
    llm=llm,
)

escritor = Agent(
    role="Escritor Técnico Senior",
    goal="Escribir una entrada de blog interesante y atractiva sobre los últimos proyectos de IA utilizando un vocabulario sencillo",
    backstory="""Eres un escritor experto en innovación técnica, especialmente en el campo de la IA y el aprendizaje automático. Sabes escribir de manera
    atractiva, interesante pero simple, directa y concisa. Sabes cómo presentar términos técnicos complicados a una audiencia general de manera 
    divertida usando palabras sencillas. SOLO usa datos recopilados de internet para el blog.""",
    verbose=True,
    allow_delegation=True,
    llm=llm,
)

traductor = Agent(
    role="Traductor",
    goal="Traducir el informe y el blog al español sin perder el formato ni el contenido",
    backstory="""Eres un traductor profesional con experiencia en la traducción de textos técnicos y artículos de blogs. Te aseguras de que la traducción 
    sea precisa, manteniendo el tono y el estilo del texto original.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

tarea_informe = Task(
    description="""ES MUY IMPORTANTE: No hacer mas de 3 busquedas. Usa y resume datos recopilados de internet para hacer un informe detallado sobre los proyectos emergentes más recientes en IA. Usa SOLO 
    datos recopilados para generar el informe. Tu respuesta final DEBE ser un informe de análisis completo, solo texto, ignora cualquier código u otra cosa 
    que no sea texto. El informe debe tener viñetas con 5-10 nuevos y emocionantes proyectos y herramientas de IA. Escribe nombres de cada herramienta y proyecto. 
    Cada viñeta DEBE contener 3 frases que se refieran a una compañía específica de IA, producto, modelo o cualquier cosa que hayas encontrado en internet. Puedes buscar en el subreddit LocalLLama entre otros.
    """,
    agent=explorador,
    expected_output="Un informe detallado sobre los proyectos emergentes más recientes en IA."
)

tarea_blog = Task(
    description="""Escribe una entrada de blog solo con texto y con un título corto pero impactante y al menos 10 párrafos. El blog debe resumir 
    el informe sobre las últimas herramientas de IA encontradas por tu compañero investigador senior. El estilo y tono deben ser atractivos y concisos, divertidos, técnicos pero también 
    usar palabras sencillas para el público en general. Nombra proyectos nuevos y emocionantes, aplicaciones y compañías en el mundo de la IA. No 
    escribas "**Párrafo [número del párrafo]:**", en su lugar, comienza el nuevo párrafo en una nueva línea. Escribe nombres de proyectos y herramientas en NEGRITA.
    SIEMPRE incluye enlaces a proyectos/herramientas/documentos de investigación. SOLO incluye información de LocalLLama.
    Para tus respuestas usa el siguiente formato markdown:
    ```
    ## [Título del post](enlace al proyecto)
    - Hechos interesantes
    - Opiniones propias sobre cómo se conecta con el tema general del boletín
    ## [Título del segundo post](enlace al proyecto)
    - Hechos interesantes
    - Opiniones propias sobre cómo se conecta con el tema general del boletín
    ```
    """,
    agent=escritor,
    expected_output="Escribir una entrada de blog interesante y atractiva sobre los últimos proyectos de IA."
)

tarea_traduccion = Task(
    description="""Traduce el informe detallado y la entrada del blog al español. Mantén el formato original y asegúrate de que la traducción sea precisa 
    y clara. El informe debe mantener las viñetas y la estructura, y el blog debe seguir el formato markdown proporcionado. Asegúrate de que todos los 
    nombres de proyectos y herramientas estén traducidos correctamente.""",
    agent=traductor,
    expected_output="Una traducción precisa y clara del informe detallado y la entrada del blog al español."
)

# instanciar grupo de agentes
crew = Crew(
    agents=[explorador, escritor, traductor],
    tasks=[tarea_informe, tarea_blog, tarea_traduccion],
    verbose=True, # se cambio el 2 por True
    process=Process.sequential,  # El proceso secuencial hará que las tareas se ejecuten una tras otra y el resultado de la anterior se pase como contenido adicional a la siguiente.
)

# ¡Haz que tu grupo trabaje!
resultado = crew.kickoff()

print("######################")
print(resultado)
