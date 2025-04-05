import openai
import json

client = openai.OpenAI(api_key="")

prompt = (
    "Gere um exemplo curto de cena de um roteiro audiovisual em inglês, "
    "incluindo descrição breve do local, diálogos curtos com dois personagens, "
    "e uma lista de objetos visíveis na cena. O retorno deve ser em formato JSON, "
    "seguindo este exemplo:\n\n"
    "{\n"
    "  \"scene\": 1,\n"
    "  \"location\": \"Cafeteria\",\n"
    "  \"time\": \"Morning\",\n"
    "  \"description\": \"A busy coffee shop filled with customers and the smell of fresh coffee.\",\n"
    "  \"dialogues\": [\n"
    "    {\"character\": \"Bob\", \"line\": \"Two espressos, please.\"},\n"
    "    {\"character\": \"Barista\", \"line\": \"Coming right up!\"}\n"
    "  ],\n"
    "  \"objects\": [\"espresso machine\", \"coffee cup\", \"table\"]\n"
    "}"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você gera cenas em formato JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=300
)

generated_scene = response.choices[0].message.content
scene_json = json.loads(generated_scene)

print(json.dumps(scene_json, indent=2))