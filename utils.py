from google import genai
from google.genai import types
API_KEY = "AIzaSyCS2ETNURnJ8KRKCN_1cyIs94FXnQXh86s"

# Only run this block for Gemini Developer API
SYSTEM_PROMPT = """
Your a help assistant who give replay to specification related question.
You should search in the provide spec files and build a small replay for the questions
like the give EXAMPLES.
Also return whether the provided question is in the document or nor.
"""
client = genai.Client(api_key=API_KEY)
def generate_response(prompt, uploaded_files):
    total_content = [prompt]
    total_content.extend(uploaded_files)
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        config=types.GenerateContentConfig(
        #     tools=ordering_system,
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
        contents=total_content,
    )
    return response.text

def create_gemini_file(file):
    uploaded_file = client.files.upload(file=file, config=dict(
    mime_type='application/pdf', display_name=file.name))
    return uploaded_file

def get_all_files_uploaded():
    return client.files.list()