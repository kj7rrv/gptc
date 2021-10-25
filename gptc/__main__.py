#!/usr/bin/env python3
import argparse
import json
import sys
import gptc

parser = argparse.ArgumentParser(description="General Purpose Text Classifier")
parser.add_argument('model', help='model to use')
parser.add_argument('-c', '--compile', help='compile raw model model to outfile', metavar='outfile')
args = parser.parse_args()

with open(args.model, 'r') as f:
    raw_model = json.load(f)
if args.compile:
    with open(args.compile, 'w+') as f:
        json.dump(gptc.compile(raw_model), f)
else:
    classifier = gptc.Classifier(raw_model)
    if sys.stdin.isatty():
        text = input('Text to analyse: ')
    else:
        text = sys.stdin.read()
    print(classifier.classify(text))
