'''Main module for GPTC.'''

import sys

def _listify(text):
    """Convert a string to a list of lemmas."""
    out = [""]

    for char in text.lower():
        if char.isalpha() or char == "'":
            out[-1] += char
        elif out[-1] != "":
            out.append("")

    return [string for string in out if string]

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
    model : dict
        A compiled GPTC model.

    Attributes
    ----------
    model : dict
        The model used.

    """

    def __init__(self, model):
        self.model = model

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
