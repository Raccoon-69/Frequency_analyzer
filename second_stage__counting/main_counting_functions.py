from _10__divide_and_rule.second_stage__counting import CountPhraseInTheText, CountWordsInTheText, ReadDFAndClearingText
from _10__divide_and_rule.tools_function import adding_dictionary_in_df


class MainCountWordsInText:
    def __init__(self):
        self.df_result = None
        self.dictionary = None
        self.token_list = None
        self.info = {
            'total_words': 0
        }

    def start_count(self, df_dict, df_text, df_names, settings):
        text_str = self.read(df_dict, df_text, df_names, settings)
        self.search(text_str)
        self.adding()
        return self.df_result

    def read(self, df_dict, df_text, df_names, settings):
        print(settings['text_path_name_extension'])
        self.dictionary, text_str, self.df_result, self.token_list = ReadDFAndClearingText().start_read(df_dict,
                                                                                                        df_text,
                                                                                                        df_names,
                                                                                                        settings)
        return text_str

    def search(self, text_str):
        phrase_list = list(self.dictionary.keys())
        phrase_list.sort(key=len, reverse=True)
        self.dictionary, self.token_list, self.info = CountPhraseInTheText().start(phrase_list, text_str,
                                                                                   self.dictionary,
                                                                                   self.token_list, self.info)
        self.dictionary, self.info = CountWordsInTheText().start(self.dictionary, self.token_list, self.info)

    def adding(self):
        self.df_result = adding_dictionary_in_df(self.df_result, self.dictionary)

