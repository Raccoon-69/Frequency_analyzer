import sys

import nltk
import pandas as pd


class ReadDFAndClearingText:

    def start_read(self, df_dict, df_text, df_names, settings):
        self.main_check(df_dict, df_text, df_names, settings)
        df_result = pd.DataFrame(columns=['KY', 'RU', 'ENG', 'GHz', 'found_words'])
        dictionary, text_str, names_list = self.main_read(df_dict, df_text, df_names, settings)
        tokens = self.clearing_text(text_str, names_list)
        return dictionary, text_str, df_result, tokens

    # ===============| read |===============
    def main_read(self, df_dict, df_text, df_names, settings):
        dict_dict = self.read_dict(df_dict)
        name_list = self.read_other_df(df_names, "Names", "name")
        text_str = self.read_other_df(df_text, "Text", "maintext") if settings['text_extension'] in (".csv", ".xlsx")\
            else df_text
        return dict_dict, text_str, name_list

    def read_dict(self, df_dict):
        dictionary = {}
        all_row = len(df_dict)
        for i, row in df_dict.iterrows():
            sys.stdout.write(f'\rDictionary reading {str(all_row)}/{str(i)}')
            dictionary[row['keyword'].lower()] = {
                "GHz": 0,
                "RUS": row['value'],
                "ENG": row['ENG'],
                "similar": {}
            }
        return dictionary

    def read_other_df(self, df, name_df, columns):
        if (name_df == 'Names' and columns == 'name') or (name_df == 'Text' and columns == 'maintext'):
            all_row = len(df)
            text = [] if name_df == "Names" else ""
            for i, row in df.iterrows():
                sys.stdout.write(f'\r{name_df} reading {str(all_row)}/{str(i)}')
                if row[columns] and type(row[columns]) == str:
                    text += [row[columns].lower()] if name_df == "Names" else f"{row[columns].lower()} "
            return text
        else:
            raise KeyError('passed arguments are invalid')
    # ======================================

    # ===========| clearing text |==========
    def clearing_text(self, text_str, names):
        # Фильтрация от цифр, имен и фамилий
        tokens_list_demo = nltk.tokenize.word_tokenize(text_str)  # Токенизация
        all_row = len(tokens_list_demo)
        tokens = []
        for i, word in enumerate(tokens_list_demo):
            sys.stdout.write(f'\rRemoval of names {str(all_row)}/{str(i)}')
            tokens += [word] if word not in names and word.isalpha() else []
        return tokens
    # ======================================

    # ============| files check |===========
    def main_check(self, df_dict, df_text, df_names, settings):
        self.dict_check(df_dict)
        self.text_check(df_text)
        self.names_check(df_names)
        self.extension_check(settings)

    def dict_check(self, df_dict):
        allowed_dict = ['keyword', 'value', 'ENG']
        if not all(column in df_dict.columns for column in allowed_dict):
            raise KeyError('column "keyword" is not defined')
        elif len(df_dict['keyword']) <= 0:
            raise TypeError('column "keyword" is empty')

    def text_check(self, df_text):
        if 'maintext' not in df_text.columns:
            raise KeyError('column "maintext" is not defined')
        elif len(df_text['maintext']) <= 0:
            raise TypeError('column "maintext" is empty')

    def names_check(self, df_names):
        if 'name' not in df_names.columns:
            raise KeyError('column "name" is not defined')
        elif len(df_names['name']) <= 0:
            raise TypeError('column "name" is empty')

    def extension_check(self, settings):
        if settings['text_extension'] not in ('.csv', '.xlsx', '.txt'):
            raise TypeError(f'extension "{settings["text_extension"]}" is not defined')
    # ======================================

