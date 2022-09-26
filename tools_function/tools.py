import os
import sys

import pandas as pd


def open_text_file(settings):
    if settings['text_extension'] == '.csv':
        df = pd.read_csv(settings['text_path_name_extension'])
        df = df.drop_duplicates('url', keep='last')
        df['keyword'] = df['maintext'].astype('str')
    elif settings['text_extension'] == '.xlsx':
        df = pd.read_excel(settings['text_path_name_extension'], sheet_name=settings['text_sheet_name'])
        df = df.drop_duplicates('url', keep='last')
        df['keyword'] = df['maintext'].astype('str')
    elif settings['text_extension'] == '.txt':
        text_file = open('drive/MyDrive/For_colab/First_text.txt', 'r')
        df = text_file.read().lower()
    else:
        raise NameError(f'\nHay, Raccoon - Wrong format selected!\n'
                        f"text_file_extension = {settings['text_extension']}\n")
    return df


def open_dictionary(settings):
    df_dictionary = pd.read_csv(settings['path_to_dictionary'], low_memory=False)
    df_dictionary['keyword'] = df_dictionary['keyword'].astype('str')
    return df_dictionary


def create_result_folder(path, folder_name):
    if not os.path.isdir(f'{path}{folder_name}'):
        os.mkdir(f'{path}{folder_name}')
        return f'{path}{folder_name}/'
    return f'{path}{folder_name}/'


def save_result_df(df, settings):
    if settings['result_extension'] == '.xlsx':
        df.to_excel(settings['result_path_name_extension'], index=settings['result_index'])
    elif settings['result_extension'] == '.csv':
        df.to_csv(settings['result_path_name_extension'], index=settings['result_index'])
    else:
        raise NameError(f'\nHay, Raccoon - Wrong format selected!\n'
                        f'result_extension = {settings["result_extension"]}\n')


def unpack(dict, key):
    GHz = dict[key]["GHz"]
    RU = dict[key]["RUS"]
    EN = dict[key]["ENG"]
    sim = dict[key]["similar"]
    return GHz, RU, EN, sim


def package(dict, GHz, RUS, ENG, similar, word):
    dict[word] = {
        "GHz": GHz,
        "RUS": RUS,
        "ENG": ENG,
        "similar": similar}
    return dict


def adding_dictionary_in_df(df, dictionary):
    # Добавление найденных слов, в конечный результат
    word_list = dictionary.keys()
    all_row = len(word_list)
    for i, word in enumerate(word_list):
        sys.stdout.write(f'\rAdding found words {str(all_row)}/{str(i)}')
        df.at[len(df)] = word, dictionary[word]['RUS'], dictionary[word]['ENG'], \
                         dictionary[word]['GHz'], dictionary[word]['similar']
    return df
