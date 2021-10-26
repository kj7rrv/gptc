# GPTC
General-purpose text classifier in Python

GPTC provides both a CLI tool and a Python library.

## CLI Tool
### Classifying text

    `python -m gptc <modelfile>`

This will prompt for a string and classify it, outputting the category on
stdout (or "None" if it cannot determine
anything).
### Compiling models

    gptc <raw model file> -c|--compile <compiled model file>

## Library
### `gptc.Classifier(model)`
Create a `Classifier` object using the given *compiled* model (as a dict, not
JSON).
#### `Classifier.classify(text)`
Classify `text` with GPTC using the model used to instantiate the
`Classifier`. Returns the category into which the text is placed (as a
string), or `None` when it cannot classify the text.
## `gptc.compile(raw_model)`
Compile a raw model (as a list, not JSON) and return the compiled model (as a
dict).

## Model format
This section explains the raw model format, which is how you should create and
edit models.

Raw models are formatted as a list of dicts. See below for the format:

    [
        {
            "text": "<text in the category>",
            "category": "<the category>"
        }
    ]

GPTC handles models as Python `list`s of `dict`s of `str`s (for raw models) or
`dict`s of `str`s and `float`s (for compiled models), and they can be stored
in any way these Python objects can be. However, it is recommended to store
them in JSON format for compatibility with the command-line tool.

## Example model
An example model, which is designed to distinguish between texts written by
Mark Twain and those written by William Shakespeare, is available in `models`.
The raw model is in `models/raw.json`; the compiled model is in
`models/compiled.json`.
