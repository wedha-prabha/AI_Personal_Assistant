from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    device_map="auto"
)

def get_oss_response(prompt):

    try:

        result = generator(
            prompt,
            max_new_tokens=100,
            truncation=True
        )

        return result[0]["generated_text"]

    except Exception as e:

        return f"Error: {str(e)}"   