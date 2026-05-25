blocked_words = [

    "make bomb",
    "hack wifi",
    "create malware"
]

def check_safety(prompt):

    for word in blocked_words:

        if word.lower() in prompt.lower():

            return False

    return True