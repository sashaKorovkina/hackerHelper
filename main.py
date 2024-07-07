import pyscreenshot as ImageGrab
import keyboard
import tempfile
from datetime import datetime
from PIL import Image
import pytesseract
from openai import OpenAI # openai version 1.1.1
import instructor

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sasha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

api_key = 'sk-proj-YOUR-API-KEY'

prompt_question = "Extract - problem statement" + 'this are some ambugious text with a coding interview problem. You need to extract the problem from the text'

prompt_solution= "Write code to solve this problem"

def ask_openai(extracted_text, prompt_question):
  client = instructor.patch(OpenAI(api_key=api_key))
  order_detail = client.chat.completions.create(
    model="gpt-4",
    messages = [
        {"role": "user", "content": prompt_question + extracted_text}
    ])
  result_string = order_detail.choices[0].message.content
  print(result_string)
  return result_string


def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def take_screenshot():
    # Get current time and format it for the filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{current_time}.png"

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png', prefix='screenshot_', dir=None) as temp_file:
        temp_filename = temp_file.name

    # Take the screenshot
    screenshot = ImageGrab.grab()

    # Save the screenshot to the temporary file
    screenshot.save(temp_filename)
    print(f"Screenshot saved as {temp_filename}")
    extract_text = ocr_image(temp_filename)
    print(f"Text extracted.")
    text = ask_openai(extract_text, prompt_question)
    ask_openai(text, prompt_solution)
    return temp_filename


def main():
    print("Press Control + S to take a screenshot")
    # Register the hotkey
    keyboard.add_hotkey('ctrl+y', take_screenshot)

    # Keep the script running
    keyboard.wait('esc')  # Press 'esc' to exit the script


if __name__ == "__main__":
    main()
