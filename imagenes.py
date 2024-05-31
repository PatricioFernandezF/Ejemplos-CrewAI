from crewai import Agent, Task, Crew, Process
import os
from langchain_openai import ChatOpenAI
from tools.crearimagen import CreateImageWithTextTool

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = "NA"

# Initialize the language model
llm = ChatOpenAI(
    model="llama3",
    base_url="http://localhost:11434/v1"
)

# Initialize the image creation tool
image_tool = CreateImageWithTextTool()

# Define the first agent to generate inspirational phrases
frases = Agent(
    role='Generador de frases inspiradoras',
    goal='Generar 1 frase inspiradora única y creativa.',
    backstory='Eres un robot especializado en crear frases inspiradoras para motivar a las personas.',
    llm=llm,
    verbose=False
)


# Define the task for generating inspirational phrases
generar_frase = Task(
    description="Generar 1 frase inspiradora única y creativa.",
    agent=frases,
    expected_output="SOLO TIENES QUE DECIR 1 frase inspiradoras en formato texto en ESPAÑOL (NO DIGAS NOTAS NI COMENTARIOS) (no mas de 7 palabras). Formato: Frase",
    tools=[],
    verbose=True
)

generar_imagen = Task(
    description="REPETIR LA FRASE DEL PASO ANTERIOR.",
    agent=frases,
    expected_output="REPETIR LA FRASE DEL PASO ANTERIOR (NO DIGAS NOTAS NI COMENTARIOS). Formato: Frase. Luego haz una imagen con tu herramienta (frase: str,color:str,bgcolor:str), pasa los colores en hexadecimal, los colores deben hacer contraste",
    tools=[image_tool],
    verbose=True
)

# Create the crew with a sequential process
crew = Crew(agents=[frases], tasks=[generar_frase,generar_imagen], process=Process.sequential, verbose=True)

# Execute the tasks
result = crew.kickoff()
print(result)
