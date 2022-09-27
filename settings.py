import os

# from google.colab import drive
# drive.mount('/content/drive')


r'''
    ============\
    | settings | ==>
    ============/
'''
main_project_folder = '/'.join(os.getcwd().split('\\')[:-1])
next_folder_to_text_files = '/Sources/for_test/'

stage = 'all'  # "first", "second", "third" or "all"

settings = {

    'original_text_title': 'test_text',
    'text_extension': '.xlsx',
    'text_sheet_name': 'Sheet1',

    'path_to_folder_with_text': f'{main_project_folder}/' if stage in ('first', 'all') else None,
    'path_to_names': f'{main_project_folder}/Sources/Names.csv',
    'path_to_dictionary': f'{main_project_folder}/Sources/for_test/Dictionary_test.csv',

    'sources_path': f'{main_project_folder}{next_folder_to_text_files}',

    'result_extension': '.xlsx',
    'result_sheet_name': 'Sheet1',
    'result_index': True,

    'number_of_part': 4,
    'start_number_of_part': 0,

    # Parameters that cannot be changed:
    'text_path_name_extension': None,
    'result_path_name_extension': None
}



''' completion stage settings: '''
r'''
    "first" - splitting one large text into smaller parts
        "number_of_part" - the number of parts into which to split the file
        (
        if number_of_part == 4 and stage == "first":
            text_file --> part_0 (text_file)
                          part_1 (text_file)
                          part_2 (text_file)
                          part_3 (text_file)
        )
    "second" - calculation of the occurrence of words in all parts of the text
        "start_number_of_part" - starting from which part of the text to calculation
        (
        if start_number_of_part == 1 and stage == "second":
            part_1 (text_file) \       / demo_dictionary_part_1 (text_file)
            part_2 (text_file) -  -->  - demo_dictionary_part_2 (text_file)
            part_3 (text_file) /       \ demo_dictionary_part_3 (text_file)
        )
    "third" - combing all parts into one and calculation the frequency as a percentage
        (
        if stage == "third":
            demo_dictionary_part_1 (text_file) \
            demo_dictionary_part_2 (text_file) -  -->  Frequency_dictionary (text_file)
            demo_dictionary_part_3 (text_file) /
        )
'''
