# Dicthon  
[![Python package](https://github.com/eyji-koike/Dicthon/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/eyji-koike/Dicthon/actions/workflows/python-package.yml)  

This library is meant to be a convenient wrapper around the [Dictonary API](https://dictionaryapi.dev/)   


### Installation:
```commandline
pip install Dicthon
```

### Support:

Currently, this library only displays english words.

## Get started:

### Instantiate a Dictionary API Entry object

To use the library, first you need to import it and then instatiate a variable.

> _Important:_ The class auto starts, you can use either the methods or the class vars to retrieve the desired result

```python
from Dicthon import Dictionary_API_Entry

myWord = Dictionary_API_Entry('hello')
```

### Examples with outputs


```python
from Dicthon import Dictionary_API_Entry

myWord = Dictionary_API_Entry('hello')

print(myWord.raw_entry)
print(myWord.get_dict_entry())
''' 
Returns the raw answer from the API in a JSON style
Just as the example: https://dictionaryapi.dev/
'''

print(myWord.antonyms)
print(myWord.get_all_antonyms())
# returns: [['bye', 'goodbye']]

print(myWord.audio_links)
print(myWord.get_all_audio_links())
# returns: ['https://api.dictionaryapi.dev/media/pronunciations/en/hello-au.mp3', 'https://api.dictionaryapi.dev/media/pronunciations/en/hello-uk.mp3']

print(myWord.definitions)
print(myWord.get_all_definitions())
# returns: ['"Hello!" or an equivalent greeting.', 'To greet with "hello".', ...]

print(myWord.definitions_with_example)
print(myWord.get_all_definitions_with_example())
# returns: [{'definition': 'A greeting (salutation) said when meeting someone or acknowledging someone’s arrival or presence.', 'example': 'Hello, everyone.'}]

print(myWord.phonetic_texts)
print(myWord.get_all_phonetic_text_representation())
# ['/həˈləʊ/', '/həˈloʊ/']

print(myWord.synonyms)
print(myWord.get_all_synonyms())
# [['greeting']]

print(myWord.parts_of_speech)
print(myWord.get_all_parts_of_speech())
# return: ['noun', 'verb', 'interjection']

print(myWord.meanings_list)
print(myWord.get_all_meanings())
'''
Returns something similar to the following
[[{'antonyms': [],
   'definitions': [{'antonyms': [],
                    'definition': '"Hello!" or an equivalent greeting.',
                    'synonyms': []}],
   'partOfSpeech': 'noun',
   'synonyms': ['greeting']},
  {'antonyms': [],
   'definitions': [{'antonyms': [],
                    'definition': 'To greet with "hello".',
                    'synonyms': []}],
   'partOfSpeech': 'verb',
   'synonyms': []}]]
'''

print(myWord.phonetics)
print(myWord.get_all_phonetics())
'''
return something like:
[[{'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/hello-au.mp3',
   'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=75797336', 
   'license': {'name': 'BY-SA 4.0', 'url': 'https://creativecommons.org/licenses/by-sa/4.0'}},
]]
'''
```

### Contributing

[Contributing Guidelines](/CONTRIBUTING.md).


