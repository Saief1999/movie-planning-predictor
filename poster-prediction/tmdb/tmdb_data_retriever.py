import requests
import os
import pandas as pd

from tmdb.constants import TMDB_API_URL
from utils.secret_manager import SecretsManager

class TmdbDataRetriever:
    """Based on TMDB CSV bulk ids. Retrieve extra data fields using the API.
    """

    def __init__(self) -> None:
        self.session = requests.Session()
        self.api_key = SecretsManager.retrieve_api_key()

    def get_images_url(self, movie_id):
        return f"{TMDB_API_URL}/movie/{movie_id}/images"

    def retrieve(self, bulk_data_path: str):
        if not os.path.isfile(bulk_data_path):
            raise Exception("Bulk data file does not exist.")

        dataframe = pd.read_csv(bulk_data_path)
        

        for movie in dataframe.values:
            id = movie[0]
            name = movie[1]
            self.session.get("")