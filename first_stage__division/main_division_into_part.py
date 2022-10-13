import pandas as pd


class MainDivisionIntoPart:
    def start_division(self, df_smi, settings):
        result_dfs_dict = self.create_df_results(settings['number_of_part']+1)
        skip_num = self.create_skip_num(len(df_smi), settings['number_of_part'] + 1)
        result_dfs_dict = self.write_in_files(df_smi, result_dfs_dict, skip_num)
        self.df_result_save(result_dfs_dict, settings)


    def create_df_results(self, num):
        result_dfs_dict = {}
        for i in range(0, num):
            result_dfs_dict[f'part_{i}'] = pd.DataFrame(
                columns=['mass_media_name', 'title', 'author', 'date_publish', 'url', 'tags', 'lang',
                         'maintext', 'scraping_time', 'maintext_hash'])  # Создание новой таблицы
        return result_dfs_dict

    def create_skip_num(len_df, count_of_part):
        step = round(len_df / count_of_part)
        skip_num = []
        for i in range(0, count_of_part):
            skip_num += [step * i]
        print(skip_num[1:])
        return skip_num[1:]

    def write_in_files(self, df, result_dfs_dict, skip_num):
        num = 0
        for i, row in df.iterrows():
            df_result = result_dfs_dict[f'part_{num}']
            df_result = self.write_to_string(df_result, row)
            result_dfs_dict[f'part_{num}'] = df_result
            if i in skip_num and len(df) > i:
                if num != len(result_dfs_dict):
                    num += 1
        return result_dfs_dict

    def write_to_string(self, df, row):
        df.at[len(df)] = row['mass_media_name'], row['title'], \
                         row['author'], row['date_publish'], \
                         row['url'], row['tags'], row['lang'], \
                         row['maintext'], row['scraping_time'], \
                         row['maintext_hash']
        return df

    def df_result_save(self, result_dfs_dict, settings):
        for df_id, name_df in enumerate(result_dfs_dict.keys()):
            df = result_dfs_dict[name_df]
            result_path_name = f"{settings['sources_path']}part_{df_id} ({settings['original_text_title']})"
            if settings['result_extension'] == '.csv':
                df.to_csv(f'{result_path_name}.csv', index=settings['result_index'])
            elif settings['result_extension'] == '.xlsx':
                df.to_excel(f'{result_path_name}.xlsx', sheet_name=settings['result_sheet_name'])
            else:
                raise NameError('\n' + '=' * 50 + '\n| Hey Raccoon, we have a file extension problem! |\n' + '=' * 50)
