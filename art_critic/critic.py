import base64
from pathlib import Path
import json
import ollama

def analyze_images():
    image_dir = Path("data/images")
    for image_path in image_dir.glob("*.jpg"):
        object_id = image_path.stem
        evaluate_image(object_id)

def evaluate_image(object_id: str):
    result = ollama.chat(
        model="llava:34b",
        messages=[
            {
                'role': 'user',
                'content': 'Describe this artwork. Return result as a JSON object with keys equal to style, subjects, color, themes. The value of each key is a list of string keywords.',
                'images': [f"data/images/{object_id}.jpg"]
            }
        ]
    )

    # llama returns results in Markdown, e.g. ```json... ```
    markdown_content = result['message']['content']
    lines = markdown_content.split('\n')
    content = '\n'.join(lines[1:-1])
    json_value = json.loads(content)
    _save_response(object_id=object_id, json_value=json_value)
    print(f"// Object ID {object_id}")
    print(json.dumps(json_value, indent=2))

def _save_response(object_id: str, json_value: str):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{object_id}.json"
    with open(output_path, "w") as f:
        json.dump(json_value, f, indent=2)
