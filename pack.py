import sys
import os
import json

if len(sys.argv) != 2:
    print('usage: pack.py <path>', file=sys.stderr)
    exit(1)

paths = os.listdir(sys.argv[1])
texts = {}

for path in paths:
    texts[path] = []
    try:
        for file in os.listdir(os.path.join(sys.argv[1], path)):
            try:
                with open(os.path.join(sys.argv[1], path, file)) as f:
                    texts[path].append(f.read())
            except Exception as e:
                print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)

raw_model = []

for category, cat_texts in texts.items():
    raw_model += [{'category': category, 'text': i} for i in cat_texts]

print(json.dumps(raw_model))
