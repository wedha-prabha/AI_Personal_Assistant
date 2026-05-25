import json

with open(
    "evaluation/prompts.json"
) as f:

    prompts=json.load(f)

for p in prompts:

    print(

        p["category"],
        p["prompt"]
    )