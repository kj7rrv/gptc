def tokenize(text):
    """Convert a string to a list of lemmas."""
    out = [""]

    for char in text.lower():
        if char.isalpha() or char == "'":
            out[-1] += char
        elif out[-1] != "":
            out.append("")

    return [string for string in out if string]
