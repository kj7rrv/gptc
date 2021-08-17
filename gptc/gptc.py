'''Main module for GPTC.'''

import sys
import spacy

nlp = spacy.load('en_core_web_sm')

def _listify(text):
    """Convert a string to a list of lemmas."""
    return [string.lemma_.lower() for string in nlp(text) if string.lemma_[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']


def compile(raw_model):
    """Compile a raw model.

    Parameters
    ----------
    raw_model : list of dict
        A raw GPTC model.

    Returns
    -------
    dict
        A compiled GPTC model.

    """

    categories = {}

    for portion in raw_model:
        text = _listify(portion['text'])
        category = portion['category']
        try:
            categories[category] += text
        except KeyError:
            categories[category] = text

    categories_by_count = {}
    
    for category, text in categories.items():
        categories_by_count[category] = {}
        for word in text:
            try:
                categories_by_count[category][word] += 1/len(categories[category])
            except KeyError:
                categories_by_count[category][word] = 1/len(categories[category])
    word_weights = {}
    for category, words in categories_by_count.items():
        for word, value in words.items():
            try:
                word_weights[word][category] = value
            except KeyError:
                word_weights[word] = {category:value}

    return word_weights


class Classifier:
    """A text classifier.

    Parameters
    ----------
    model : dict or list
        A compiled or raw GPTC model. Please don't use raw models except
        during development.

    Attributes
    ----------
    model : dict
        The model used. This is always a compiled model.

    """

    def __init__(self, model, supress_uncompiled_model_warning=False):
        if type(model) == dict:
            self.model = model
        else:
            self.model = compile(model)
            if not supress_uncompiled_model_warning:
                print('WARNING: model was not compiled', file=sys.stderr)
                print('This makes everything slow, because compiling models takes far longer than using them.', file=sys.stderr)
        self.warn = supress_uncompiled_model_warning

    def classify(self, text):
        """Classify text.

        Parameters
        ----------
        text : str
            The text to classify

        Returns
        -------
        str or None
            The most likely category, or None if no guess was made.

        """

        model = self.model
        text = _listify(text)
        probs = {}
        for word in text:
            try:
                for category, value in model[word].items():
                    try:
                        probs[category] += value
                    except KeyError:
                        probs[category] = value
            except KeyError:
                pass
        try:
            return sorted(probs.items(), key=lambda x: x[1])[-1][0]
        except IndexError:
            return None
