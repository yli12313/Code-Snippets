"""
Description: Data pipeline with Luigi template. 

Date: Wed. 1/31/24 @ 5:07 PM EST
"""

# Importing the required libraries: luigi, pandas, luigi.contrib
import luigi
import pandas as pd
from luigi.contrib import s3

# Defining an ExtractDataTask().
class ExtractDataTask(luigi.Task):
    # After executing this task, the output is 'raw_data.csv'.
    def output(self):
        return luigi.LocalTarget('raw_data.csv')

    def run(self):
        # Creating a dataframe for reference. 'self.output().path' is mapped
        # to the path of the output, which for this code is 'raw_data.csv'.
        data = {'Name': ['Tom', 'Nick', 'John', 'Tom'], 'Age': [20, 21, 19, 20]}
        df = pd.DataFrame(data)
        df.to_csv(self.output().path, index=False)

# Defining a TransformDataTask().
class TransformDataTask(luigi.Task):
    # The order of the tasks: ExtractDataTask(luigi.Task) --> TransformDataTask(luigi.Task).
    def requires(self):
        return ExtractDataTask()

    # After executing this task, the output is 'transformed_data.csv'.
    def output(self):
        return luigi.LocalTarget('transformed_data.csv')

    # 'self.input().path' in 'TransformDataTask()' will return the path of the output of 
    # 'ExtractDataTask()', which is 'raw_data.csv'.
    def run(self):
        df = pd.read_csv(self.input().path)
        df = df.drop_duplicates()
        df.to_csv(self.output().path, index=False)

# Defining a LoadDataTask().
class LoadDataTask(luigi.Task):
    # The order of the tasks: TransformDataTask(luigi.Task) --> LoadDataTask(luigi.Task).
    def requires(self):
        return TransformDataTask()

    # 1. 'self.input().path' in 'LoadDataTask()' will return the path of the output of 
    # 'TransformDataTask()', which is 'transform_data.csv'.

    # 2. Load the transformed data to a data warehouse, a database, etc. Here we'll just 
    # print it out.
    def run(self):
        df = pd.read_csv(self.input().path)
        print(df)

if __name__ == '__main__':
    # Note the use of [].
    luigi.build([LoadDataTask()])
