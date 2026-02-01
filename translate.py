from openai import OpenAI

client = OpenAI()

def translate(text: str) -> str:
    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"You are a professional technical translator. Translate accurately into natural Japanese."},
            {"role":"user","content":text}
        ],
        temperature=0.1
    )
    return r.choices[0].message.content.strip()
