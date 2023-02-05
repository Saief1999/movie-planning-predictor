import os
from datetime import date
import gzip
import shutil

from tmdb.enums import ExportType
from tmdb.constants import TMDB_EXPORT_URL, TMDB_EXPORT_EXTENSION, TMDB_EXPORT_EXTENSION_ZIPPED
from utils.file_downloader import FileDownloader


class TmdbBulkRetriever:
    """Retrieves bulk Data from TMDB
    """

    def __init__(self, dest_folder: str) -> None:

        self.dest_folder = dest_folder

        if not os.path.exists(self.dest_folder):
            os.mkdir(self.dest_folder)

        self.downloader = FileDownloader()

    def get_daily_export_url(self, export_date: date, export_type: ExportType = ExportType.MOVIE) -> str:
        """Generates the URL to get item ids from TMDB.

        Args:
            export_date (date, optional): day of data export. Defaults to None.
            export_type (ExportType, optional): export type. Defaults to ExportType.MOVIE.

        Returns:
            str: URL of the file to download.
        """

        formatted_date: str = export_date.strftime("%m_%d_%Y")

        file_path: str = f"{export_type.value}_ids_{formatted_date}.{TMDB_EXPORT_EXTENSION_ZIPPED}"

        return f"{TMDB_EXPORT_URL}/{file_path}"

    def unzip_file(self, in_path, out_path):
        with gzip.open(in_path, 'rb') as f_in:
            with open(out_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def retrieve_movies(self, export_date: date = None, custom_name: str = None) -> str:
        """_summary_

        Args:
            export_date (date, optional): the date of the data export. Defaults to None (Current Date).
            custom_name (str, optional): a custom name for the file. Defaults to None ().

        If export_date is not provided. Current Date is used.
        if custom_name is not provided. Current Date as yyyy-mm-dd is used.

        Returns:
            str: bulk data path
        """
        if (export_date is None):
            export_date = date.today()

        url = self.get_daily_export_url(export_date)

        # If no custom name is provided. We default to the current date
        if custom_name is not None:
            basename = custom_name
        else:
            basename = export_date.strftime('%Y-%m-%d')

        filename = f"{basename}.{TMDB_EXPORT_EXTENSION_ZIPPED}"

        print("Retrieving bulk data...")
        self.downloader.download(url, self.dest_folder, filename)

        print("bulk data retrieved.")

        # Name of the file after unzipping
        unzip_name = f"{basename}.{TMDB_EXPORT_EXTENSION}"

        filepath: str = f"{self.dest_folder}/{filename}"
        unzip_path: str = f"{self.dest_folder}/{unzip_name}"

        print("Unzipping bulk data...")
        self.unzip_file(filepath, unzip_path)

        os.remove(filepath)
        print("Bulk data unzipped.")

        return unzip_path
