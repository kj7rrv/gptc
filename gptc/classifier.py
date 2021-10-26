import gptc.tokenizer

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
        text = gptc.tokenizer.tokenize(text)
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
