class Dictionary_API_Entry:
    """
    Instantiate a Dictionary API entry. https://dictionaryapi.dev/
    This instance will query the entry on the API and enables you
    to access the following:
    ✔︎ List of Audio Pronunciation Links\n
    ✔︎ List of Antonyms\n
    ✔︎ List of Synonyms\n
    ✔︎ List of Word Classes\n
    ✔︎ List of Definitions\n
    ✔︎ List of Definitions with Example\n
    ✔︎ List of Phonetic Text Representations\n
    ✔︎ Raw JSON entry\n
    :param word: The word to search.
    :type word: str.
    """

    def __init__(self, word: str):
        self.raw_entry = []
        self.word = word
        self.audio_links = []
        self.antonyms = []
        self.synonyms = []
        self.phonetic_texts = []
        self.phonetics = []
        self.definitions = []
        self.parts_of_speech = []
        self.meanings_list = []
        self.definitions_with_example = []
        self.__set_up__()

    def __set_up__(self):
        self.get_dict_entry()
        self.get_all_meanings()
        self.get_all_parts_of_speech()
        self.get_all_phonetics()
        self.get_all_phonetic_text_representation()
        self.get_all_synonyms()
        self.get_all_antonyms()
        self.get_all_definitions()
        self.get_all_definitions_with_example()
        self.get_all_audio_links()

    def get_dict_entry(self):
        """
        Based on the word defined in the initialization,
        do a GET request in the API.

        :return: the API answer.
        :rtype: list
        """
        import requests
        model_link = f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}'
        entry = requests.get(model_link)
        self.raw_entry = entry.json()
        return self.raw_entry

    def get_all_meanings(self):
        """
        A list with lists of meanings

        :return: list with lists of meanings.
        :rtype: list
        """
        for item in self.raw_entry[:]:
            if 'meanings' in item.keys():
                self.meanings_list.append(item['meanings'])
        return self.meanings_list

    def get_all_parts_of_speech(self):
        """
        A list with all classes the word has.

        :return: list word classes.
        :rtype: list
        """
        for meanings in self.meanings_list[:]:
            for meaning in meanings[:]:
                if 'partOfSpeech' in meaning.keys() and meaning['partOfSpeech'] not in self.parts_of_speech:
                    self.parts_of_speech.append(meaning['partOfSpeech'])
        return self.parts_of_speech

    def get_all_definitions(self):
        """
        A list with all the word definitions

        :return: list with definitions.
        :rtype: list
        """
        for parts_of_speech in self.meanings_list[:]:
            for part_of_speech in parts_of_speech[:]:
                if ('definitions' in part_of_speech.keys()) and type(part_of_speech['definitions']) == list:
                    for definition in part_of_speech['definitions']:
                        if 'definition' in definition.keys() and definition['definition'] != [] and definition['definition'] not in self.definitions:
                            self.definitions.append(definition['definition'])
        return self.definitions

    def get_all_definitions_with_example(self):
        """
        A list with all the word definitions which have an example.

        :return: list definition and example.
        :rtype: list
        """

        examples = []
        for parts_of_speech in self.meanings_list[:]:
            for part_of_speech in parts_of_speech[:]:
                if ('definitions' in part_of_speech.keys()) and type(part_of_speech['definitions']) == list:
                    for definition in part_of_speech['definitions']:
                        if ('example' in definition.keys()) and (definition['example'] != []) and (definition['example'] not in examples):
                            examples.append(definition['example'])
                            self.definitions_with_example.append(
                                {'definition': definition['definition'], 'example': definition['example']})
        return self.definitions_with_example

    def get_all_phonetics(self):
        """
        A list with all the word phonetics and links.

        :return: list with phonetics.
        :rtype: list
        """
        for phonetics in self.raw_entry[:]:
            if 'phonetics' in phonetics.keys():
                self.phonetics.append(phonetics['phonetics'])

        return self.phonetics

    def get_all_phonetic_text_representation(self):
        """
        A list with all the phonetic representations the word has.

        :return: list with phonetic text representation.
        :rtype: list
        """
        for phonetics in self.phonetics[:]:
            for phonetic in phonetics:
                if 'text' in phonetic.keys() and phonetic['text'] not in self.phonetic_texts:
                    self.phonetic_texts.append(phonetic['text'])
        return self.phonetic_texts

    def get_all_synonyms(self):
        """
        A list with the synonyms found for the word

        :return: list with synonyms.
        :rtype: list
        """
        for parts_of_speech in self.meanings_list[:]:
            for part_of_speech in parts_of_speech[:]:
                if ('definitions' in part_of_speech.keys()) and type(part_of_speech['definitions']) == list:
                    for definition in part_of_speech['definitions']:
                        if 'synonyms' in definition.keys() and definition['synonyms'] != []:
                            self.synonyms.append(definition['synonyms'])
                if ('antonyms' in part_of_speech.keys()) and part_of_speech['synonyms'] != [] and part_of_speech['synonyms'] not in self.synonyms:
                    self.synonyms.append(part_of_speech['synonyms'])
        return self.synonyms

    def get_all_antonyms(self):
        """
        A list with the antonyms found for the word

        :return: list with antonyms.
        :rtype: list
        """
        for parts_of_speech in self.meanings_list[:]:
            for part_of_speech in parts_of_speech[:]:
                if ('definitions' in part_of_speech.keys()) and type(part_of_speech['definitions']) == list:
                    for definition in part_of_speech['definitions']:
                        if 'antonyms' in definition.keys() and definition['antonyms'] != []:
                            self.antonyms.append(definition['antonyms'])
                if ('antonyms' in part_of_speech.keys()) and part_of_speech['antonyms'] != [] and part_of_speech['antonyms'] not in self.antonyms:
                    self.antonyms.append(part_of_speech['antonyms'])
        return self.antonyms

    def get_all_audio_links(self):
        """
        A list with the audio pronunciation links

        :return: list with links.
        :rtype: list
        """
        for entry in self.raw_entry[:]:
            for phonetics in entry['phonetics']:
                if phonetics['audio'] not in self.audio_links and phonetics['audio'] != '':
                    self.audio_links.append(phonetics['audio'])
        return self.audio_links
