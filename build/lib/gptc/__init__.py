#!/usr/bin/env python3
import sys
import spacy

nlp = spacy.load('en_core_web_sm')

def listify(text):
    return [string.lemma_.lower() for string in nlp(text) if string.lemma_[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']


def compile(raw_model):
    model = {}

    for portion in raw_model:
        text = listify(portion['text'])
        category = portion['category']
        for word in text:
            try:
                model[category].append(word)
            except:
                model[category] = [word]
            model[category].sort()
    all_models = [ { 'text': model, 'stopword': i/10} for i in range(0, 21) ]
    for test_model in all_models:
        correct = 0
        classifier = Classifier(test_model)
        for text in raw_model:
            if classifier.check(text['text']) == text['category']:
                correct += 1
        test_model['correct'] = correct
        print('tested a model')
    best = all_models[0]
    for test_model in all_models:
        if test_model['correct'] > best['correct']:
            best = test_model
    del best['correct']
    return best
    return {'text': model}


class Classifier:
    def __init__(self, model, supress_uncompiled_model_warning=False):
        if type(model['text']) == dict:
            self.model = model
        else:
            self.model = compile(model)
            if not supress_uncompiled_model_warning:
                print('WARNING: model was not compiled', file=sys.stderr)
                print('In development, this is OK, but precompiling the model is preferred for production use.', file=sys.stderr)
        self.warn = supress_uncompiled_model_warning

    def check(self, text):
        model = self.model
        stopword_value = 0.5
        try:
            stopword_value = model['stopword']
        except:
            pass
        stopwords = spacy.lang.en.stop_words.STOP_WORDS
        model = model['text']
        text = listify(text)
        probs = {}
        for word in text:
            for category in model.keys():
                for catword in model[category]:
                    if word == catword:
                        weight = ( stopword_value if word in stopwords else 1 ) / len(model[category])
                        try:
                            probs[category] += weight 
                        except:
                            probs[category] = weight
        most_likely = ['unknown', 0]
        for category in probs.keys():
            if probs[category] > most_likely[1]:
                most_likely = [category, probs[category]]
        return most_likely[0]
