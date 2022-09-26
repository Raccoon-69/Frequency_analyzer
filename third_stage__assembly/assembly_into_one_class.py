import json

import pandas as pd
from _10__divide_and_rule.tools_function import package, adding_dictionary_in_df


class AssemblyIntoOne:

    def start_assembly(self, settings):
        dictionary = self.compiling_all_files_into_one_dictionary(settings)
        df_result = pd.DataFrame(columns=['KY', 'RU', 'ENG', 'GHz', 'found_words'])
        df_result = adding_dictionary_in_df(df_result, dictionary)
        return df_result

    def compiling_all_files_into_one_dictionary(self, settings):
        result_dict = {}
        for i in range(settings['start_number_of_part'], settings['number_of_part']+1):
            if settings['text_extension'] == '.csv':
                text_file_name = f'part_{i} ({settings["original_text_title"]}).csv'
                df = pd.read_csv(settings['sources_path'] + text_file_name)
            elif settings['text_extension'] == '.xlsx':
                text_file_name = f'part_{i} ({settings["original_text_title"]}).xlsx'
                df = pd.read_excel(settings['sources_path'] + text_file_name,
                                   sheet_name=settings['text_sheet_name'])
            else:
                raise NameError(f'\nHay, Raccoon - Wrong format selected!\n'
                                f'text_extension = {settings["text_extension"]}\n')
            result_dict = self.assemble(df, result_dict)
        return result_dict

    def assemble(self, df, dictionary):
        for i, row in df.iterrows():
            if row['KY'] in dictionary.keys():
                dictionary[row['KY']]['GHz'] += row['GHz']
                dictionary = self.merge_dictionaries_similar(dictionary, row['KY'], row['found_words'])
            else:
                dictionary = package(dictionary, row['GHz'], row['RU'], row['ENG'], row['found_words'], row['KY'])
        return dictionary

    def merge_dictionaries_similar(self, dictionary, word, second_similar):
        if "'" in second_similar:
            for i in range(0, second_similar.count("'")):
                second_similar = second_similar.replace("'", '"')
        second_similar = json.loads(second_similar)
        first_similar = dictionary[word]['similar']
        if "'" in first_similar:
            for i in range(0, first_similar.count("'")):
                first_similar = first_similar.replace("'", '"')
        if type(first_similar) == str:
            first_similar = json.loads(first_similar)
        for word_in_similar in second_similar.keys():
            if word_in_similar in first_similar.keys():
                first_similar[word_in_similar] += second_similar[word_in_similar]
            else:
                first_similar[word_in_similar] = second_similar[word_in_similar]
        dictionary[word]['similar'] = first_similar
        return dictionary
