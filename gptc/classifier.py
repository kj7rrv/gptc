import gptc.tokenizer, gptc.compiler, gptc.exceptions
import warnings

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
        try:
            model_version = model['__version__']
        except:
            model_version = 1

        if model_version == 1:
            self.model = model
        else:
            # The model is an unsupported version
            try:
                raw_model = model['__raw__']
            except:
                raise gptc.exceptions.UnsupportedModelError('this model is unsupported and does not contain a raw model for recompiling')

            warnings.warn("model needed to be recompiled on-the-fly; please re-compile it and use the new compiled model in the future")
            self.model = gptc.compiler.compile(raw_model)

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
