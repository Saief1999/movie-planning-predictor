
import os
from clint.textui import progress
import json
import pandas as pd


class TmdbBulkCleaner:
    """Cleans bulk data from TMDB.
    """

    def __init__(self, show_progress=True) -> None:
        """Cleans bulk data from TMDB.

        Args:
            show_progress (bool, optional): Show progress or not. Defaults to True.
        """

        self.show_progress = show_progress

    def clean(self, in_path: str, out_path: str = None) -> None:
        """
        1. Remove adult movies
        2. Remove videos
        3. Convert to csv for easier manipulation and smaller size

        Args:
            in_path (str): input bulk data path.
            out_path (str): output CSV file path. Defaults to None.

        If out_path is not provided. The same name/path will be used

        Raises:
            Exception
        """
        # Check whether file exists or not
        if not os.path.isfile(in_path):
            raise Exception("Bulk data file does not exist.")

        if out_path is None:
            [path_no_ext, _] = os.path.splitext(in_path)
            [base_path, filename] = os.path.split(path_no_ext)
            out_path = f"{base_path}/{filename}.csv"

        lines = []
        cleaned_lines = []

        with open(in_path, "r") as file:
            lines = file.readlines()

        print("Cleaning Bulk Data...")

        for line in progress.bar(lines, every=500, hide=False):
            data = json.loads(line)

            # Make sure it's not a video/ adult movi
            if (not data["adult"] and not data["video"]):
                cleaned_lines.append([data["id"], data["original_title"]])

        # Create file
        dataframe = pd.DataFrame(data=cleaned_lines, columns=[
                                 'id', 'original_title'])

        dataframe.to_csv(out_path, encoding='utf-8', index=False)

        print("Cleaned CSV file created.")

        return out_path


if __name__ == "__main__":

    bulk_cleaner = TmdbBulkCleaner()
    in_path = f"{os.path.dirname(__file__)}/data/2023-02-05.json"
    bulk_cleaner.clean(in_path)
