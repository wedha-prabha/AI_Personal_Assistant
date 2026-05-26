import json
import os

CHAT_HISTORY_PATH = os.path.join(os.path.dirname(__file__), "chat_history.json")


def save_chat(user, response, assistant="Unknown"):
    entry = {"assistant": assistant, "input": user, "output": response}

    try:
        if os.path.exists(CHAT_HISTORY_PATH):
            with open(CHAT_HISTORY_PATH, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []
    except Exception:
        history = []

    history.append(entry)

    with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_chat_history():
    try:
        if os.path.exists(CHAT_HISTORY_PATH):
            with open(CHAT_HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    return []
