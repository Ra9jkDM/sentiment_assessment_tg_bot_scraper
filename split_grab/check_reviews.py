import json

with open('reviews/3.json', 'r') as f:
    r = json.loads(f.read())
    print(r)
