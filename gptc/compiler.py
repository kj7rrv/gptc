import gptc.tokenizer

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
        text = gptc.tokenizer.tokenize(portion['text'])
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

    word_weights['__version__'] = 1
    word_weights['__raw__'] = raw_model

    return word_weights