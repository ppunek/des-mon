import re
import requests
import json

file_id = '195zPsYhg57YLXUtvzwZ55Y459I1wzYdf'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

response = requests.get(url)
conteudo = response.text

def is_scene_heading(line):
    return re.match(r'^\d+\s+(INT\.|EXT\.)', line.strip())

def is_character_name(line):
    return line.strip().isupper() and len(line.strip()) > 0 and len(line.strip().split()) <= 4

def parse_script(text):
    lines = text.splitlines()
    scenes = []
    current_scene = None
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if is_scene_heading(line):
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                "scene": line.strip(),
                "content": []
            }
            i += 1
            continue

        elif line.startswith('                        ') and is_character_name(line.strip()):
            character = line.strip()
            i += 1
            dialogue_lines = []
            while i < len(lines) and lines[i].startswith('              '):
                dialogue_lines.append(lines[i].strip())
                i += 1
            if current_scene and dialogue_lines:
                current_scene["content"].append({
                    "type": "dialogue",
                    "character": character,
                    "line": " ".join(dialogue_lines)
                })
            continue

        elif line.strip() and current_scene:
            desc_lines = [line.strip()]
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line == "" or is_scene_heading(lines[i]) or (lines[i].startswith('                        ') and is_character_name(next_line)):
                    break
                desc_lines.append(next_line)
                i += 1
            current_scene["content"].append({
                "type": "description",
                "text": " ".join(desc_lines)
            })
            continue

        i += 1

    if current_scene:
        scenes.append(current_scene)

    return scenes

roteiro_processado = parse_script(conteudo)

with open("THE MENU.json", "w", encoding="utf-8") as f:
    json.dump(roteiro_processado, f, indent=2, ensure_ascii=False)

print("✅ Salvo THE MENU.json")
