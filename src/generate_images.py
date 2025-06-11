import os
import re
import json
import openai
import requests

def extract_style_and_prompt(image_prompt):
    match = re.match(r"\[(.*?)\]\s*(.+)", image_prompt.strip())
    if match:
        style, prompt = match.groups()
        return style.lower(), prompt.strip()
    else:
        return "natural", image_prompt.strip()

def process_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    scenes = data.get("scenes", [])
    for idx, scene in enumerate(scenes, 1):
        full_prompt = scene.get("image_prompt", "").strip()
        style, prompt = extract_style_and_prompt(full_prompt)
        results.append({
            "scene_idx": idx,
            "style": style,
            "prompt": prompt
        })

    return results

def generate_image(openai_client, prompt_kwargs, output_path):
    style = prompt_kwargs.get("style")
    prompt = prompt_kwargs.get("prompt")
    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            style=style,
            response_format="url"
        )
        url = response.data[0].url
        image_data = requests.get(url).content
        with open(output_path, "wb") as f:
            f.write(image_data)
        return True
        # print(f"✅ 저장 완료: {output_path}")
    except Exception as e:
        print(f"❌ 실패 ({prompt}): {e}")
        return False

def json_to_images(openai_client, base_path="articles"):
    print("\n", "="*20, "\n이미지 변환 중...")
    for root, dirs, files in os.walk(base_path):
        processed_any = 0
        for file in files:
            if not file.endswith(".json"):
                continue
            
            json_path = os.path.join(root, file)
            prompts = process_json(json_path)
            if not prompts or len(prompts) != 6:
                print(f"⚠️ 프롬프트 없음: {json_path}")
                continue

            output_dir = os.path.splitext(json_path)[0]
            os.makedirs(output_dir, exist_ok=True)
            
            num_generated_imgs = 0
            for prompt in prompts:
                filename = os.path.join(output_dir, f"{prompt.get('scene_idx')}.png")
                is_generated = generate_image(openai_client, prompt, filename)
                if is_generated:
                    num_generated_imgs += 1
            
            if len(prompts) == num_generated_imgs:
                processed_any += 1
        
        if processed_any:
            if len(files) == processed_any:
                print(f"✅ {os.path.basename(root)} 처리 완료")
            else:
                print(f"⚠️ {os.path.basename(root)}: {processed_any}개 처리 완료")
                
if __name__ == "__main__":
    json_to_images()
