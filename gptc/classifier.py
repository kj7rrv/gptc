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

    def confidence(self, text):
        """Classify text with confidence.

        Parameters
        ----------
        text : str
            The text to classify

        Returns
        -------
        dict
            {category:probability, category:probability...} or {} if no words
            matching any categories in the model were found

        """

        model = self.model

        text = gptc.tokenizer.tokenize(text)
        probs = {}
        for word in text:
            try:
                total = sum(model[word].values())
                for category, value in model[word].items():
                    try:
                        probs[category] += value / total
                    except KeyError:
                        probs[category] = value / total
            except KeyError:
                pass
        total = sum(probs.values())
        probs = {category: value/total for category, value in probs.items()}
        return probs

    def classify(self, text):
        """Classify text.

        Parameters
        ----------
        text : str
            The text to classify

        Returns
        -------
        str or None
            The most likely category, or None if no words matching any
            category in the model were found.

        """
        probs = self.confidence(text)
        try:
            return sorted(probs.items(), key=lambda x: x[1])[-1][0]
        except IndexError:
            return None
