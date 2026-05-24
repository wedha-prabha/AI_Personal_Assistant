from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

def get_oss_response(prompt):

    result = generator(
        prompt,
        max_new_tokens=150,
        truncation=True
    )

    return result[0]["generated_text"]