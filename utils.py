from google import genai
from google.genai import types
API_KEY = "AIzaSyCS2ETNURnJ8KRKCN_1cyIs94FXnQXh86s"

# Only run this block for Gemini Developer API
SYSTEM_PROMPT = """
Your a help assistant who give replay to specification related question.
You should search in the provide spec files and build a small replay for the questions
like the give EXAMPLES.

EXAMPLES:
    Question 1:
        HDPE fittings should be injected and molded. Segmented fittings shown on the Technical Data Sheet to be removed and the supplier to resubmit new Technical Data Sheet without segmented fittings.
    Replay 1:
        Please note that proposed HDPE fittings are injection molded & data sheet is attached for the injection molded fittings.
    Question 2:
        Revise parameters to be for all working scenarios (Qmin / Qmax / Qavg /with upstream and downstream pressures for each flow). Then forward to vendor to revise calculations/charts.
    Replay 2:
        Sizing Calculation is revised based on consultant RFI letter dated 23.01.2023.
"""
client = genai.Client(api_key=API_KEY)
def generate_response(prompt, uploaded_files):
    total_content = [prompt]
    total_content.extend(uploaded_files)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        config=types.GenerateContentConfig(
        #     tools=ordering_system,
            system_instruction=SYSTEM_PROMPT,
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