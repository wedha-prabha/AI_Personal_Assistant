import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

FRONTIER_MODEL = os.getenv("FRONTIER_MODEL", "models/gemini-2.5-flash")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_frontier_response(prompt):
    if not prompt or not prompt.strip():
        return "Please enter a prompt to send to the Frontier assistant."

    try:
        chat = client.chats.create(model=FRONTIER_MODEL)
        response = chat.send_message(prompt)
        return response.text or "No response returned from Frontier."
    except Exception as e:
        return f"Error: {str(e)}"