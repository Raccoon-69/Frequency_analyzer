import sys

import nltk

from Frequency_analyzer.tools_function import unpack, package


class CountWordsInTheText:

    def start(self, dictionary, tokens, info):
        filtered_word_freq, words_in_dict, words_in_text = self.filter_and_sort_tokens(tokens, dictionary)
        dictionary, words_in_text, info = self.word_search(dictionary, words_in_dict, words_in_text,
                                                           filtered_word_freq, info)
        dictionary, info = self.adding_new_word_in_dict(words_in_text, filtered_word_freq, dictionary, info)
        return dictionary, info

    def filter_and_sort_tokens(self, tokens, dictionary):
        fdist1 = nltk.FreqDist(tokens)
        filtered_word_freq = dict(
            (word, freq) for word, freq in fdist1.items() if (word.isalnum() and not word.isdigit() and freq != 1))
        words_in_dict = list(dictionary.keys())
        words_in_text = list(filtered_word_freq.keys())
        words_in_dict.sort(key=len, reverse=True)
        words_in_text.sort(key=len, reverse=True)
        return filtered_word_freq, words_in_dict, words_in_text

    def word_search(self, dictionary, words_in_dict, words_in_text, filtered_word_freq, info):
        all_row = len(words_in_dict)
        for i, one_word_in_dict in enumerate(words_in_dict):
            sys.stdout.write(f'\rWords search {str(all_row)}/{str(i)}')
            if len(one_word_in_dict) not in (0, 1) and " " not in list(one_word_in_dict):
                matches, found_words, ghz = [], {}, 0
                matches_list = self.search_words_in_dict(one_word_in_dict, words_in_text)  # поиск слов в словаре
                ghz, found, words_in_text = self.match_handling(matches_list, found_words, ghz,
                                                                filtered_word_freq, words_in_text)
                ghz_int, RUS, ENG, similar_list = unpack(dictionary, one_word_in_dict)
                dictionary = package(dictionary, ghz, RUS, ENG, found_words, one_word_in_dict)
                info['total_words'] += ghz
        return dictionary, words_in_text, info

    def search_words_in_dict(self, one_word_in_dict, words_in_text):
        matches = []
        for word in words_in_text:
            if len(word) > len(one_word_in_dict) or len(one_word_in_dict) - len(word) < len(word) + 8:
                continue
            elif word.startswith(one_word_in_dict):
                matches.append(word)
        return matches

    def match_handling(self, matches, found, ghz, filtered_word_freq, words_in_text):
        for match in matches:
            ghz += filtered_word_freq[match]
            if match not in found.keys():
                found[match] = filtered_word_freq[match]
            words_in_text.remove(match)
        return ghz, found, words_in_text

    def adding_new_word_in_dict(self, words_in_text, filtered_word_freq, dictionary, info):
        # Добавление новых слов в конечный результат
        new_words = words_in_text  # Слова, которые не были удалены из списка, являются новыми
        all_row = len(new_words)
        for i, word in enumerate(new_words):
            sys.stdout.write(f'\rAdding new words {str(all_row)}/{str(i)}')
            good = self.filter_new_word(word)  # фильтрация от иероглифов, английских слов и 1-2-х буквенных слов
            if good:
                info, dictionary = self.count_and_add_in_dictionary(word, info, dictionary, filtered_word_freq)
        return dictionary, info

    def filter_new_word(self, word):
        # Фильтрация новых слов
        white_list = list("ячсмитьбюфывaапролджэйцукенгшщзхъёөүңy")
        if len(word) >= 4:
            for i in range(0, 2):
                if list(word)[i] not in white_list:
                    return False
            return True
        return False

    def count_and_add_in_dictionary(self, word, info, dictionary, filtered_word_freq):
        info['total_words'] += filtered_word_freq[word]
        dictionary = package(dictionary, filtered_word_freq[word], '-', '-', '{'
                               + f'"{word}": {filtered_word_freq[word]}' + '}', word)
        return info, dictionary
