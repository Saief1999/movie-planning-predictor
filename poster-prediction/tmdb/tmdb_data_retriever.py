import requests
import os
import pandas as pd
import numpy as np

from clint.textui import progress

from tmdb.constants import TMDB_API_URL
from utils.secret_manager import SecretsManager


class TmdbDataRetriever:
    """Based on TMDB CSV bulk ids. Retrieve extra data fields using the API.
    """

    def __init__(self, show_progress=True) -> None:
        """Based on TMDB CSV bulk ids. Retrieve extra data fields using the API.

        Args:
            show_progress (bool, optional): Show progress or not. Defaults to True.
        """
        self.session = requests.Session()
        self.api_key = SecretsManager.retrieve_api_key()
        self.show_progress = show_progress

    def get_images_url(self, movie_id):
        return f"{TMDB_API_URL}/movie/{movie_id}/images"

    def retrieve(self, bulk_data_path: str, chunk=None, out_path: str = None):
        if not os.path.isfile(bulk_data_path):
            raise Exception("Bulk data file does not exist.")

        # Handle case where output path is not provided
        if out_path is None:
            [path_no_ext, _] = os.path.splitext(bulk_data_path)
            [base_path, filename] = os.path.split(path_no_ext)
            out_path = f"{base_path}/{filename}-data.csv"

        dataframe = pd.read_csv(bulk_data_path)
        values = []

        # Handle case where chunk path is not provided
        if chunk is None:
            values = dataframe.values
        else:
            if chunk > len(dataframe.values):
                raise Exception("Chunk bigger than total movie count.")
            values = dataframe.values[:chunk]

        new_data: list[str] = []

        # Go through movies, create list of data
        for movie in progress.bar(values, every=1, hide=not self.show_progress):
            id = movie[0]
            response = self.session.get(self.get_images_url(
                id), params={'api_key': self.api_key})

            if response.status_code != 200:
                raise Exception("Problem Sending API Request.")

            data = response.json()
            posters = data["posters"]

            if (not posters or len(posters) == 0):
                continue

            for poster in posters:
                new_data.append(list(np.hstack([movie, poster["file_path"]])))

        # Create file
        dataframe = pd.DataFrame(data=new_data, columns=[
                                 'id', 'original_title', "poster_url"])

        dataframe.to_csv(out_path, encoding='utf-8', index=False)

        print("CSV with data created.")
