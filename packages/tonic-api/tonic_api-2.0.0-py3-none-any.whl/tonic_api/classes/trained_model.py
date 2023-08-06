import pandas as pd

from typing import List

from tonic_api.services.models import ModelService
from tonic_api.classes.model import Model
from tonic_api.classes.httpclient import HttpClient


class TrainedModel:
    """Wrapper class for accessing trained models.

    Attributes
    ----------
    id : str
        id of model
    job_id : str
        id of training job
    workspace_id : str
        id of workspace
    model :  Model
        the Tonic Model object
    model_service : ModelService
        service for accessing Tonic Model
    """

    def __init__(
        self, id: str, job_id: str, workspace_id: str, model: Model, client: HttpClient
    ):
        self.id = id
        self.job_id = job_id
        self.workspace_id = workspace_id
        self.model = model
        self.client = client
        self.model_service = ModelService(client)

    def sample(self, num_rows: int=1) -> pd.DataFrame:
        """Generates synthetic samples from trained_model.

        Parameters
        ----------
        num_rows : int, optional
            Number of rows to generate.

        Returns
        -------
        pandas.DataFrame
            A dataframe of synthetic data.
        """
        res = self.model_service.sample(self.id, num_rows)
        return self.__convert_to_df(res)

    def sample_source(self, num_rows: int=1):
        """Generates samples from source data.

        Parameters
        ----------
        num_rows : int, optional
            Number of rows to generate.

        Returns
        -------
        pandas.DataFrame
            A dataframe of real data.

        Examples
        --------
        >>> synth_df = model.sample(1000)
        """
        res = self.model_service.sample_source(
            self.workspace_id, self.model.query, num_rows
        )
        columns = res["columns"]
        if len(columns) == 0:
            raise Exception("No data returned from source database")

        n_rows_returned = len(columns[0]["data"])
        converted_res = [{} for _ in range(n_rows_returned)]

        if n_rows_returned < num_rows:
            print(
                "Not enough rows in source destination to sample, limiting to "
                + str(n_rows_returned)
                + " rows."
            )

        for col in columns:
            data = col["data"]
            for idx, val in enumerate(data):
                converted_res[idx][col["columnName"]] = val
        return self.__convert_to_df(converted_res)

    def get_numeric_columns(self) -> List[str]:
        """Returns list of columsn with numeric encodings.
        
        Returns
        -------
        List[str]
        """

        return [
            col
            for (col, encoding) in self.model.encodings.items()
            if encoding == "Numeric"
        ]

    def get_categorical_columns(self) -> List[str]:
        """Returns list of columns with categorical encodings.
        
        Returns
        -------
        List[str]
        """
        return [
            col
            for (col, encoding) in self.model.encodings.items()
            if encoding == "Categorical"
        ]

    def __convert_to_df(self, sample_response):
        schema = self.__get_schema()
        df = pd.DataFrame(sample_response)
        df = self.__conform_df_to_schema(df, schema)
        return df

    def __get_schema(self):
        schema = self.model_service.get_schema(self.workspace_id, self.model.query)
        ordered_schema = self.__convert_schema_to_ordered_col_list(schema)
        return ordered_schema

    def __convert_schema_to_ordered_col_list(self, schema):
        return [
            obj["columnName"]
            for obj in sorted(schema, key=lambda v: v["ordinalPosition"])
        ]

    def __conform_df_to_schema(self, df, schema):
        return df.reindex(schema, axis=1)

    def describe(self):
        """Prints description of trained model."""
        print("Trained Model: [" + self.id + "]")
        print("Job ID: " + self.job_id)
        print("Workspace ID: " + self.workspace_id)
        print("Model: ")
        self.model.describe()
