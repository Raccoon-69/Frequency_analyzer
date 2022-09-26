import re
import sys

from _10__divide_and_rule.tools_function import unpack, package


class CountPhraseInTheText:

    def start(self, phrase_list, text, dictionary, tokens, info):
        for i, phrase in enumerate(phrase_list):
            sys.stdout.write(f'\rPhrase search {str(len(phrase_list))}/{str(i)}')
            if " " in list(phrase):
                dictionary, tokens, info = self.search_phrase_in_the_text_and_save_to_dictionary(text, phrase,
                                                                                                 dictionary, tokens,
                                                                                                 info)
        return dictionary, tokens, info

    def search_phrase_in_the_text_and_save_to_dictionary(self, text, phrase, dictionary, tokens, info):
        found_phrases_list = self.found_phrases(text, phrase)
        info['total_words'] += len(found_phrases_list)
        GHz, RUS, ENG, similar_dict = unpack(dictionary, phrase)
        remove_word, similar_dict, GHz = self.count_and_save_remove_words(found_phrases_list, similar_dict, GHz)
        tokens = self.remove_tokens(remove_word, tokens)
        dictionary = package(dictionary, GHz, RUS, ENG, similar_dict, phrase)
        return dictionary, tokens, info

    def found_phrases(self, text, phrase):
        pattern = self.create_pattern(phrase)
        found_phrases_list = re.findall(pattern, text)
        return found_phrases_list

    def create_pattern(self, phrase):
        word_list = phrase.split(' ')
        start = fr"\b{word_list[0]}\w*"
        continuation = [fr"\s{word_list[i + 1]}\w*" for i in range(0, list(phrase).count(' '))]
        return start + ''.join(continuation)

    def count_and_save_remove_words(self, found_phrases_list, similar_dict, ghz):
        remove_word = []
        for found_phrase in found_phrases_list:
            similar_dict[found_phrase] = 1 if found_phrase not in similar_dict.keys() else similar_dict[
                                                                                               found_phrase] + 1
            ghz += 1
            remove_word += found_phrase.split(' ')
        return remove_word, similar_dict, ghz

    def remove_tokens(self, remove_word, tokens):
        for word in remove_word:
            if word in tokens:
                tokens.remove(word)
        return tokens
