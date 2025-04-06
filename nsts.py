import re
import requests
import json

file_id = '1Yevi4dvJ1O5IHn8fKXM31bm0Nmlk8EzS'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

response = requests.get(url)
conteudo = response.text

def is_scene_heading(line):
    return line.strip().startswith(('INT.', 'EXT.'))

def is_character_name(line):
    return line.strip().isupper() and 1 <= len(line.strip().split()) <= 4

def parse_script(text):
    lines = text.splitlines()
    scenes = []
    current_scene = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if is_scene_heading(line):
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                "scene": line,
                "content": []
            }
            i += 1
            continue

        elif is_character_name(line):
            character = line
            i += 1
            dialogue_lines = []
            while i < len(lines) and lines[i].strip() and not is_character_name(lines[i]) and not is_scene_heading(lines[i]):
                dialogue_lines.append(lines[i].strip())
                i += 1
            if current_scene and dialogue_lines:
                current_scene["content"].append({
                    "type": "dialogue",
                    "character": character,
                    "line": " ".join(dialogue_lines)
                })
            continue

        elif line and current_scene:
            desc_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not is_character_name(lines[i]) and not is_scene_heading(lines[i]):
                desc_lines.append(lines[i].strip())
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

with open("THE SHINING.json", "w", encoding="utf-8") as f:
    json.dump(roteiro_processado, f, indent=2, ensure_ascii=False)

print("Salvo THE SHINING.json")