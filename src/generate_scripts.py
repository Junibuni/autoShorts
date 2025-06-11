PROMPT_TEMPLATE = """
최신 뉴스 기사를 제공할거야. 뉴스 기사를 참고해서 유튜브 쇼츠 영상 대본을 만들어줘.

다음 기준을 적용해서 작성해:
1. 각 scene 마다 image_prompt 는 영어로 자세하게 작성해야 해: 쇼츠에 알맞는 이미지를 생성하기 위한 프롬프트를 작성해 - 극사실적으로 만드는 것이 적합하면 [vivid] 태그를, 그렇지 않으면 [natural] 태그를 프롬프트 처음에 작성해줘. (예시: [vivid] A woman bus driver).
2. 친근한 말투 및 반말로 작성해: 빠른 정보전달 쇼츠에 알맞는 말투로 사용.
3. 톤은 유쾌하고 흥미로운 해설 스타일로, 핵심 정보(사건의 주요 장면, 인물, 의미 등)를 중심으로 짧고 임팩트 있게 구성해.
4. 이모지는 사용하지 말고, 텍스트로만 작성해.
5. 도입 3초를 ‘질문’ 혹은 ‘충격적 사실’로 시작해.
6. 마지막 2초에 자연스러운 구독·좋아요 유도 문구(부드럽게): 해당 scene 이미지는 뉴스와 관련된 장면을 모사해.
7. 영상 길이는 30초 내외야.
8. scenes 는 총 6장면이 나와야 해.
9. hashtag 는 영상과 관련된 키워드로 5~7개 추천해줘.

아래 json 포맷으로 작성해.
{
'title': 제목 텍스트,
'scenes': [
{
'image_prompt': 영상에서 보여줄 이미지에 대한 이미지 생성/서치용 프롬프트,
'script': 스크립트
},
{
'image_prompt': 영상에서 보여줄 이미지에 대한 이미지 생성/서치용 프롬프트,
'script': 스크립트
},
...
]
'hashtag': ["#hashtag1", "#hashtag2", ...]
}

아래는 뉴스 기사야:

```text
{}
```
"""

# def generate_script(article_text: str) -> str:
#     prompt = PROMPT_TEMPLATE.format(article=article_text.strip())
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7,
#         max_tokens=800,
#     )
    
#     return response["choices"][0]["message"]["content"]

# def process_all_articles():
#     for topic in os.listdir(INPUT_DIR):
#         topic_path = os.path.join(INPUT_DIR, topic)
#         if not os.path.isdir(topic_path):
#             continue

#         output_topic_dir = os.path.join(OUTPUT_DIR, topic)
#         os.makedirs(output_topic_dir, exist_ok=True)

#         for filename in os.listdir(topic_path):
#             if not filename.endswith(".md"):
#                 continue

#             input_path = os.path.join(topic_path, filename)
#             with open(input_path, "r", encoding="utf-8") as f:
#                 article = f.read()

#             script = generate_script(article)

#             output_file = os.path.join(output_topic_dir, filename.replace(".md", ".txt"))
#             with open(output_file, "w", encoding="utf-8") as f:
#                 f.write(script)

#             print(f"✅ {topic}/{filename} 처리 완료")