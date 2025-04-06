from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform
from google.oauth2 import service_account
import json

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

model = GenerativeModel("gemini-1.5-flash-preview-0514")

prompt = """
Generate a short synthetic movie script based on the following JSON format, in English, with rich descriptions of objects and scenery:

[
  {
    "scene": "EXT. BEACH AT SUNSET - DAY - WIDE SHOT",
    "content": [
      {
        "type": "description",
        "text": "The sun sets on the horizon. The sound of waves is constant. A couple walks hand in hand along the shore."
      },
      {
        "type": "dialogue",
        "character": "ANNA",
        "line": "It's so peaceful here... feels like time stands still."
      },
      {
        "type": "dialogue",
        "character": "RAFAEL",
        "line": "Maybe because we want it to."
      }
    ]
  },
  {
    "scene": "INT. ANNA'S LIVING ROOM - NIGHT - MEDIUM SHOT",
    "content": [
      {
        "type": "description",
        "text": "The room is dimly lit. Anna sits on the couch with a cup of tea."
      },
      {
        "type": "dialogue",
        "character": "ANNA",
        "line": "Do you think we made the right choice?"
      },
      {
        "type": "dialogue",
        "character": "RAFAEL (OFF)",
        "line": "We always do... even if we only realize it later."
      }
    ]
  }
]

Follow this structure, return 2 to 4 scenes with a mix of descriptions and dialogues. Respond only with valid JSON format.
"""

response = model.generate_content(prompt)
texto = response.text.strip()

if texto.startswith("```json"):
    texto = texto.removeprefix("```json").strip()
if texto.endswith("```"):
    texto = texto.removesuffix("```").strip()

try:
    dados = json.loads(texto)
    with open("ROTEIRO_SINTETICO.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

except json.JSONDecodeError as e:
    print("Erro")
