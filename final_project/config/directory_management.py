import os
import pandas as pd

class DirectoryManagement:

    def __init__(self, *args, **kwargs):
        self.path_base = kwargs.get('folder_data_base',
                                    '/Users/khanhnn/Developer/DE/AI4E_DE_05/final_project/output_data')
        self.ensure_directory_exists(self.path_base)

    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @property
    def folder_output_path(self):
        return self.path_base

    def save_data_to_csv(self, data, file_name):
        file_path = os.path.join(self.folder_output_path, file_name)
        directory = os.path.dirname(file_path)
        self.ensure_directory_exists(directory)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f'Data saved to {file_path}')

    def load_data_from_csv(self, file_name):
        file_path = os.path.join(self.folder_output_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} does not exist.')

        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')

    def save_data_benchmark(self, data, file_name):
        self.save_data_to_csv(data, os.path.join('benchmark', file_name))

    def load_data_benchmark(self, file_name):
        return self.load_data_from_csv(os.path.join('benchmark', file_name))

    def save_universities_data(self, data, file_name):
        self.save_data_to_csv(data, os.path.join('universities', file_name))

    def load_universities_data(self, file_name):
        return self.load_data_from_csv(os.path.join('universities', file_name))

    def save_data_exam_result(self, data, file_name):
        self.save_data_to_csv(data, os.path.join('exam_result', file_name))

    def load_data_exam_result(self, file_name):
        return self.load_data_from_csv(os.path.join('exam_result', file_name))