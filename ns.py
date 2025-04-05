import re
import json
import requests

#Ler do Google Drive
file_id = '1Yevi4dvJ1O5IHn8fKXM31bm0Nmlk8EzS'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

response = requests.get(url)
conteudo = response.text 

#Funções de parsing
def is_scene_heading(line):
    return line.strip().startswith(('INT.', 'EXT.'))

def is_character_name(line):
    return line.strip().isupper() and 1 <= len(line.strip().split()) <= 4

def parse_script(text):
    lines = text.splitlines()
    scenes = []
    current_scene = None
    current_char = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if is_scene_heading(line):
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                "scene": line,
                "description": "",
                "dialogue": []
            }
            current_char = None

        elif is_character_name(line):
            current_char = line
            j = i + 1
            dialogue_lines = []
            while j < len(lines) and lines[j].strip() and not is_character_name(lines[j]) and not is_scene_heading(lines[j]):
                dialogue_lines.append(lines[j].strip())
                j += 1
            if current_scene and current_char and dialogue_lines:
                current_scene["dialogue"].append({
                    "character": current_char,
                    "line": " ".join(dialogue_lines)
                })
            i = j - 1

        elif line and current_scene:
            current_scene["description"] += " " + line

        i += 1

    if current_scene:
        scenes.append(current_scene)

    return scenes

#Processar e salvar
roteiro_processado = parse_script(conteudo)

with open("shining_parsed_from_drive.json", "w", encoding="utf-8") as f:
    json.dump(roteiro_processado, f, indent=2, ensure_ascii=False)

print("✅ Roteiro processado com sucesso! Salvo como shining_parsed.json")
