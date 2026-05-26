import os
from dotenv import load_dotenv

load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")

langfuse_client = None
if LANGFUSE_PUBLIC_KEY:
    try:
        import langfuse

        langfuse_client = langfuse.get_client(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            base_url=LANGFUSE_BASE_URL,
        )
    except Exception:
        langfuse_client = None


def log_trace(prompt, response, assistant_name="Unknown"):
    lines = [
        f"Assistant: {assistant_name}",
        f"Prompt: {prompt}",
        f"Response: {response}",
    ]

    if langfuse_client is not None:
        try:
            langfuse_client.start_observation(
                name="assistant_interaction",
                as_type="generation",
                input=prompt,
                output=response,
                model=assistant_name,
            )
            trace_url = langfuse_client.get_trace_url()
            if trace_url:
                lines.append(f"Langfuse trace URL: {trace_url}")
        except Exception as e:
            lines.append(f"Langfuse logging failed: {e}")
    else:
        lines.append("Langfuse not configured or unavailable.")

    output = "\n".join(lines)
    print(output)
    return output
