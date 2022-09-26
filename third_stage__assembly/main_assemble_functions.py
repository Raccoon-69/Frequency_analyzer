from Frequency_analyzer.third_stage__assembly import FrequencyCalculation, AssemblyIntoOne
from Frequency_analyzer.tools_function import save_result_df


class MainMergeAllDfAndCalculateFrequency:

    def __init__(self):
        self.df_result = None
        self.dictionary = None
        self.info = {}

    def start_assembly(self, settings):
        self.assembly(settings)
        self.calculation()
        save_result_df(self.df_result, settings)

    def assembly(self,  settings):
        self.dictionary = AssemblyIntoOne().start_assembly(settings)

    def calculation(self):
        self.df_result, self.info = FrequencyCalculation().start_calculate(self.dictionary, self.info)

    def end(self):
        TextOutput().for_end(self.info, self.df_result)
