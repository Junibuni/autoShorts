import os
import json
from json_repair import repair_json

PROMPT_TEMPLATE = """
최신 뉴스 기사를 제공할거야. 뉴스 기사를 참고해서 유튜브 쇼츠 영상 대본을 만들어줘.

다음 기준을 적용해서 작성해:
1. 각 scene 마다 image_prompt 는 영어로 자세하게 작성해야 해: 쇼츠에 알맞는 이미지를 생성하기 위한 프롬프트를 작성해 - 극사실적으로 만드는 것이 적합하면 [vivid] 태그를, 그렇지 않으면 [natural] 태그를 프롬프트 처음에 작성해줘. (예시: [vivid] A woman bus driver).
2. 친근한 말투 및 반말로 작성해: 정보전달 쇼츠에 알맞는 말투로 사용.
3. 톤은 유쾌하고 흥미로운 해설 스타일로, 친구에게 말하듯이
4. 내용은 핵심 정보(사건의 주요 장면, 인물, 의미 등)를 중심으로 임팩트 있게 구성해: 사실 전달이 목적이기 때문에 인물, 내용, 숫자를 정확하고 자세하게 모사해줘.
5. 이모지는 어떤 경우에도 절대로 사용하지 마. 텍스트 이외의 시각적 기호(이모지, 이모티콘 등)는 모두 금지야.
6. 도입 3초를 ‘질문’ 혹은 ‘충격적 사실’로 시작해.
7. 마지막 2초에 자연스러운 구독·좋아요 유도 문구(부드럽게): 해당 scene 이미지는 뉴스와 관련된 장면을 모사해.
8. 영상 길이는 30초 내외야.
9. scenes 는 총 6장면이 나와야 해.
10. hashtag 는 영상과 관련된 키워드로 5~7개 추천해줘.

아래 json 포맷으로 작성해.
{{
'title': 제목 텍스트,
'scenes': [
{{
'image_prompt': 영상에서 보여줄 이미지에 대한 이미지 생성/서치용 프롬프트,
'script': 스크립트
}},
{{
'image_prompt': 영상에서 보여줄 이미지에 대한 이미지 생성/서치용 프롬프트,
'script': 스크립트
}},
...
]
'hashtag': ["#hashtag1", "#hashtag2", ...]
}}

아래는 뉴스 기사야:

```text
{}
```
"""

def generate_script_to_json(openai_client, article):
    client = openai_client
    prompt = PROMPT_TEMPLATE.format(article)

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )
    
    reply = response.output_text

    # 마크다운 제거
    reply = reply.strip().strip("```json").strip("```").strip()
    # # 작은따옴표 제거
    # reply_string = reply.replace("'", '"')
    
    # json 형식으로 변경
    try:
        reply_json = json.loads(repair_json(reply))
        return reply_json
    except Exception as e:
        print(e, '\n', reply)
        return {}

def articles_to_script(openai_client, article_path="articles"):
    print("\n", "="*20, "\n프롬프트 작성 중...")
    file_type = ".md"
    for root, dirs, files in os.walk(article_path):
        processed_any = 0
        for file in files:
            if file.endswith(file_type):
                md_path = os.path.join(root, file)

                with open(md_path, 'r', encoding='utf-8') as f:
                    article = f.read()

                reply_json = generate_script_to_json(openai_client, article)

                json_path = os.path.splitext(md_path)[0] + ".json"
                with open(json_path, 'w', encoding='utf-8') as jf:
                    json.dump(reply_json, jf, ensure_ascii=False, indent=2)

                processed_any += 1

        if processed_any:
            if len([f for f in os.listdir(root) if f.endswith(file_type)]) == processed_any:
                print(f"✅ {os.path.basename(root)} 처리 완료")
            else:
                print(f"⚠️ {os.path.basename(root)}: {processed_any}개 처리 완료")