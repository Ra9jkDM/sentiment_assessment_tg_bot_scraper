import json

with open('reviews/0', 'r') as f:
    r = json.loads(f.read())
    print(r)
