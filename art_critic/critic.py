import base64
from pathlib import Path
from openai import OpenAI
import json


def evaluate_image(object_id: str):
    base64_image = _encode_image(object_id=object_id)

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this artwork. Return result as a JSON object with keys equal to style, subjects, color, themes. The value of each key is a list of string keywords.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    json_value = json.loads(response.choices[0].message.content)
    _save_response(object_id=object_id, json_value=json_value)
    print(f"// Object ID {object_id}")
    print(json.dumps(json_value, indent=2))

def _save_response(object_id: str, json_value: str):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{object_id}.json"
    with open(output_path, "w") as f:
        json.dump(json_value, f, indent=2)


def _encode_image(object_id: str, directory: str = "data/images") -> str:
    image_dir = Path(directory)

    image_path = next((file_path for file_path in image_dir.iterdir()
                      if file_path.stem == object_id), None)

    if image_path is None:
        raise FileNotFoundError(f"No image found with id {
                                object_id} in {directory}")

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
