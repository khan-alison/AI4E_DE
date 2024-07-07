import os
import pandas as pd


class DirectoryManagement:

    def __init__(self, *args, **kwargs):
        self.path_base = kwargs.get('folder_data_base',
                                    '/Users/khanhnn/Developer/DE/AI4E_DE_05/final_project/output_data')
        self.ensure_directory_exists(self.path_base)

    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    @property
    def folder_output_path(self):
        return self.path_base

    def save_data_to_csv(self, data, file_name):
        self.ensure_directory_exists(self.folder_output_path)
        file_path = os.path.join(self.folder_output_path, file_name)
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
        benchmark_path = os.path.join(self.folder_output_path, 'benchmark')
        self.ensure_directory_exists(benchmark_path)
        file_path = os.path.join(benchmark_path, file_name)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f'Data saved to {file_path}')

    def load_data_benchmark(self, file_name):
        benchmark_path = os.path.join(self.folder_output_path, 'benchmark')
        self.ensure_directory_exists(benchmark_path)
        file_path = os.path.join(benchmark_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} does not exist.')

        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')

    def save_universities_data(self, data, file_name):
        universities_path = os.path.join(self.folder_output_path, 'universities')
        self.ensure_directory_exists(universities_path)
        file_path = os.path.join(universities_path, file_name)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f'Data saved to {file_path}')

    def load_universities_data(self, file_name):
        benchmark_path = os.path.join(self.folder_output_path, 'universities')
        self.ensure_directory_exists(benchmark_path)
        file_path = os.path.join(benchmark_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} does not exist.')

        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')

    def save_data_exam_result(self, data, file_name):
        benchmark_path = os.path.join(self.folder_output_path, 'exam_result')
        self.ensure_directory_exists(benchmark_path)
        file_path = os.path.join(benchmark_path, file_name)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f'Data saved to {file_path}')

    def load_data_exam_result(self, file_name):
        benchmark_path = os.path.join(self.folder_output_path, 'exam_resul')
        self.ensure_directory_exists(benchmark_path)
        file_path = os.path.join(benchmark_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} does not exist.')

        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')