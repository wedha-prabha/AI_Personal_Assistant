import torch
from transformers import pipeline

MODEL_NAME = "sshleifer/tiny-gpt2"

generator = None

def get_generator():
    device = 0 if torch.cuda.is_available() else -1
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        device=device,
        dtype=dtype,
    )


def get_oss_response(prompt):
    global generator
    if generator is None:
        try:
            generator = get_generator()
        except Exception as e:
            return f"Error initializing OSS model: {e}"

    if not prompt or not prompt.strip():
        return "Please enter a prompt for the Open Source assistant."

    try:
        result = generator(
            prompt,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.1,
            return_full_text=False,
            truncation=True,
        )
        return result[0]["generated_text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"   