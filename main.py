import os

import nltk
import pandas as pd

from Frequency_analyzer.fourth_stage__calculation import FrequencyCalculation
from Frequency_analyzer.third_stage__assembly import AssemblyIntoOne
from first_stage__division import MainDivisionIntoPart
from second_stage__counting import MainCountWordsInText
from tools_function import create_result_folder, open_text_file, open_dictionary, save_result_df
from settings import settings, stage
import openpyexcel

# ===============| start functions |===============
def start_division_into_part(settings):
    if settings['number_of_part'] > 1:
        settings['text_path_name_extension'] = settings['sources_path'] + settings['original_text_title'] \
                                               + settings['text_extension']
        df_text = open_text_file(settings)
        result_folder_name = f'first_stage_result__{settings["original_text_title"]}'
        result_path = create_result_folder(settings['sources_path'], result_folder_name)
        settings['sources_path'] = result_path
        MainDivisionIntoPart().start_division(df_text, settings)
    else:
        print('In the first stage "number_of_part" cannot be less than or equal to 1')


def start_count_words(settings):
    nltk.download('punkt')
    if settings['number_of_part'] == 1:
        df_names = pd.read_csv(settings['path_to_names'])
        df_dictionary = open_dictionary(settings)
        settings['sources_path'] += f'second_stage_result ({settings["original_text_title"]})'
        count_the_words_in_the_text_and_save_result(settings, df_names, df_dictionary)
    else:
        df_names = pd.read_csv(settings['path_to_names'])
        df_dictionary = open_dictionary(settings)
        result_folder_name = f'second_stage_result__{settings["original_text_title"]}/'
        result_path = create_result_folder(settings['sources_path'], result_folder_name)
        sources_folder_name = f'first_stage_result__{settings["original_text_title"]}/'
        text_path = settings['sources_path'] + sources_folder_name
        for i in range(settings['start_number_of_part'], settings['number_of_part']+1):
            print(f'i = {i}')
            settings['text_path_name_extension'] = text_path \
                                                   + f'part_{i} ({settings["original_text_title"]})' \
                                                   + f'{settings["text_extension"]}'
            settings['result_path_name_extension'] = result_path \
                                                     + f'part_{i} ({settings["original_text_title"]})' \
                                                     + f'{settings["result_extension"]}'
            count_the_words_in_the_text_and_save_result(settings, df_names, df_dictionary)


def start_assemble(settings):
    result_name = f'demo_frequency_dictionary ({settings["original_text_title"]}){settings["result_extension"]}'
    settings['result_path_name_extension'] = settings['sources_path'] + result_name
    if settings['number_of_part'] != 1:
        settings["sources_path"] += f'second_stage_result__{settings["original_text_title"]}/'
    df_result = AssemblyIntoOne().start_assembly(settings)
    save_result_df(df_result, settings)


def start_percent_calculation(settings):
    result_name = f'Frequency_dictionary ({settings["original_text_title"]}){settings["result_extension"]}'
    settings['result_path_name_extension'] = settings['sources_path'] + result_name
    df_dictionary = open_dictionary(settings)
    df_result = FrequencyCalculation().start_calculate(df_dictionary, settings)
    save_result_df(df_result, settings)
# =================================================


# ===============| addition |===============
def count_the_words_in_the_text_and_save_result(settings, df_names, df_dictionary):
    df_text = open_text_file(settings)
    if len(df_text['maintext']) != 0:
        df_result = MainCountWordsInText().start_count(df_dictionary, df_text, df_names, settings)
        df_result = df_result.sort_values("GHz", ascending=False)
        save_result_df(df_result, settings)


def settings_restart(settings):
    from settings import main_project_folder, next_folder_to_text_files
    settings['sources_path'] = f'{main_project_folder}{next_folder_to_text_files}'
    return settings
# ==========================================


# ==========| start |==========>
if __name__ == '__main__':
    if stage == 'first':
        start_division_into_part(settings)
    elif stage == 'second':
        start_count_words(settings)
    elif stage == 'third':
        start_assemble(settings)
    elif stage == 'fourth':
        start_percent_calculation(settings)
    elif stage == 'demo':
        start_division_into_part(settings)
        settings = settings_restart(settings)
        start_count_words(settings)
        settings = settings_restart(settings)
        start_assemble(settings)
    else:
        print(f'Error: stage = {stage}')
