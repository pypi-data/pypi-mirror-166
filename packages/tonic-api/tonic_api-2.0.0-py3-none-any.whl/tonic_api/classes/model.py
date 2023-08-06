class Model:
    """
    Class to store necessary metadata for a given model.

    Parameters
    ----------
    id : str
        Model id, comes from the workspace json/dictionary.

    model_json : dict
        Model json, comes from the workspace json/dictionary.
    """
    def __init__(self, id: str, model_json: dict):
        self.id = id
        self.name = model_json["name"]
        self.query = model_json["query"]
        self.parameters = model_json["nnModelConfig"]
        self.encodings = model_json["columnEncodings"]

    def describe(self):
        """Print model metadata - id, query, parameters (model config), encodings.
        """
        print("Model: " + self.name + " [" + self.id + "]")
        print("Query: " + self.query)
        print("Parameters: " + str(self.parameters))
        print("Column Encodings: " + str(self.encodings))
