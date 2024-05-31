from PIL import Image, ImageDraw, ImageFont
import io,os
import base64
from crewai_tools import BaseTool
from datetime import datetime

# Define la función que crea la imagen con la frase
def create_image_with_text(frase, color, bgcolor):
    print(frase)
    text = '"'+frase+'"'
    background_color = bgcolor
    font_size = 40
    font_color = color
    max_width = 780  # Máximo ancho del texto dentro de la imagen

    # Create a new blank image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color=background_color)

    # Initialize the drawing object
    draw = ImageDraw.Draw(image)

    # Load a font in italic
    try:
        font = ImageFont.truetype("ariali.ttf", font_size)  # ariali.ttf is the italic version of Arial
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)  # Fallback to normal Arial if italic is not available
        except IOError:
            font = ImageFont.load_default()

    # Dividir el texto en líneas que se ajusten al ancho máximo
    def split_text(text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    lines = split_text(text, font, max_width)
    
    # Calcular la altura total del texto
    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    
    # Calcular la posición inicial del texto para centrarlo verticalmente
    y = (height - text_height) / 2

    # Dibujar cada línea de texto
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width, line_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        x = (width - text_width) / 2
        draw.text((x, y), line, font=font, fill=font_color)
        y += line_height

    # Save the image to a buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Ensure the directory exists
    directory = "imagenes"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the image with a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.join(directory, f"image_{timestamp}.png")
    image.save(image_filename)
    
    return True

# Define la herramienta de CREW AI
class CreateImageWithTextTool(BaseTool):
    name: str = "Crear imagen"
    description: str = "Crea una imagen con el texto"

    def _run(self, frase: str,color:str,bgcolor:str):
        frase=frase.replace('"','')
        color=color.replace('"','')
        bgcolor=bgcolor.replace('"','')
        create_image_with_text(frase,color,bgcolor)

        return True
