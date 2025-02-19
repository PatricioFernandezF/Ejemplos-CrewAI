import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"


# Initialize the language model
llm = ChatOpenAI(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)


# Define the Narrative Writer agent
narrative_writer = Agent(
    role="Escritor",
    goal="Escribir relatos ambientados en la segunda guerra mundial con no más de 250 palabras.",
    backstory="Eres un talentoso escritor conocido por tu habilidad para crear historias novelizadas cautivadoras.",
    llm=llm,
    allow_delegation=False,
    verbose=False
)

# Define the Data Verifier agent
data_verifier = Agent(
    role="Verificador de informacion",
    goal="Verificar la precisión de los hechos y datos históricos utilizados en el relato.",
    backstory="Eres un experto en historia con un ojo agudo para los detalles y la precisión de los datos.",
    llm=llm,
    allow_delegation=False,
    verbose=False
)


# Define the tasks
initial_narrative_task = Task(
    description="Escribir un relato ambientado en la segunda guerra mundial. (No más de 250 palabras).",
    expected_output="Un Relato en Español.",
    agent=narrative_writer
)

verification_task = Task(
    description="Verificar la precisión de los hechos y datos históricos utilizados en la narrativa EN ESPAÑOL.",
    expected_output="Un informe en Español.",
    agent=data_verifier
)

editing_task = Task(
    description="Reescribir el relato editando el texto para garantizar la coherencia, claridad y corrección gramatical (NO AGREGUES COMENTARIOS ADICIONALES). Además si hay algun dato incorrecto en el informe quitalo (Si es ficcion no lo quites)",
    expected_output="Un RELATO en español (NO COMENTES NADA).",
    agent=narrative_writer
)


# Create the crew with all agents and tasks
crew = Crew(
    agents=[narrative_writer, data_verifier],
    tasks=[initial_narrative_task, verification_task, editing_task],
    process=Process.sequential,  # Execute tasks sequentially
    verbose=False
)

# Kickoff the project
result = crew.kickoff()

print(result)
