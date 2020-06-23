import pandas as pd


class AdWordsAPIInsightsMapper:

    @classmethod
    def map(cls, fields, df):
        df = df.where(df != ' --', None)
        df = df.where(pd.notnull(df), None)

        for field in fields:
            if field.conversion_function is not None:
                df[field.name] = df[field.name].apply(field.conversion_function)
        return df
