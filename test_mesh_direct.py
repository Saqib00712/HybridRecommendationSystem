from openai import OpenAI

client = OpenAI(
    base_url="https://api.meshapi.ai/v1",
    api_key="rsk_01KZ22JN0Y8M71FVN85NBYWVVA"
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # Try this model instead
        messages=[
            {"role": "user", "content": "Say hello in one sentence"}
        ],
        max_tokens=50
    )
    print("✅ Success:", response.choices[0].message.content)
except Exception as e:
    print("❌ Error:", e)