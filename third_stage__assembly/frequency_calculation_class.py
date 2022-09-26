import sys
from decimal import getcontext, Decimal


class FrequencyCalculation:

    def start_calculate(self, df_result, info):
        all_percent = 0
        info = self.counting_word_in_dictionary(df_result, info)
        df_result, info, all_percent = self.percent_calculation(df_result, info, all_percent)
        self.found_row(df_result, info, all_percent)
        return df_result, info

    def counting_word_in_dictionary(self, df_result, info):
        words_count = 0
        for i, row in df_result.iterrows():
            words_count += row['GHz']
        info['total_words'] = words_count
        return info

    def percent_calculation(self, df_result, info, all_percent):
        # расчет встречаемости в %
        all_row = len(df_result)
        getcontext().prec = 24  # Точность вычислений при делении
        one_percent = Decimal(info['total_words']) / Decimal(100)  # Расчет одного процента
        word_count = 0
        for i, row in df_result.iterrows():
            word_count += row['GHz']
            sys.stdout.write(f'\rPercent calculation {str(all_row)}/{str(i)}')
            frequency_calculation = Decimal(row['GHz']) / Decimal(one_percent)  # Расчет частоты встречаемости в %
            all_percent += frequency_calculation  # Суммирование строчки
            df_result.at[i, "GHz"] = frequency_calculation  # Запись в файл % встречаемости
        print(f'\nword_count = {word_count}')
        print(f'len_df = {len(df_result)}\n')
        return df_result, info, all_percent

    def found_row(self, df_result, info, all_percent):
        # поиск процентов слов, для знания текста
        df_result = df_result.sort_values("GHz", ascending=False)
        percent_80, percent_90, percent_95 = self.persent_claculation_80_90_95(all_percent)
        bool_80, bool_90, bool_95 = True, True, True
        all_row_percent_f, info["len_word"] = 0, 0
        all_row = len(df_result)
        for i, row in df_result.iterrows():
            sys.stdout.write(f'\rFound 80/90/95% {str(all_row)}/{str(i)}')
            all_row_percent_f += row['GHz']
            if all_row_percent_f > percent_80 and bool_80:
                bool_80, info["p80"] = False, str(i)
            elif all_row_percent_f > percent_90 and bool_90:
                bool_90, info["p90"] = False, str(i)
            elif all_row_percent_f > percent_95 and bool_95:
                bool_95, info["p95"] = False, str(i)
            elif row['GHz'] == 0:
                info["len_word"] = str(i)
                break

    def persent_claculation_80_90_95(self, all_percent):
        percent_80 = (Decimal(all_percent) / Decimal(100)) * Decimal(80)
        percent_90 = (Decimal(all_percent) / Decimal(100)) * Decimal(90)
        percent_95 = (Decimal(all_percent) / Decimal(100)) * Decimal(95)
        return percent_80, percent_90, percent_95
