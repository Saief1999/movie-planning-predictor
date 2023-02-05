import requests
from clint.textui import progress


class FileDownloader:
    """
    Downloads a File from a link
    """

    def __init__(self, show_progress=True) -> None:
        """Downloads a File from a link

        Args:
            show_progress (bool, optional): Show progress or not. Defaults to True.
        """

        self.session = requests.Session()
        self.show_progress = show_progress

    def download(self, url: str, dest_folder: str, name: str = "file", ):
        """downloads a file

        Args:
            url (str): url of file
            dest_folder (str): destination folder
            name (str, optional): filename. Defaults to "file".
        """

        response = self.session.get(url, stream=self.show_progress)
        filepath = f"{dest_folder}/{name}"
        if response.status_code == 200:
            if not self.show_progress:
                with open(filepath, 'wb') as f:
                    f.write(response.content)

            else:
                total_length = int(response.headers.get('content-length'))

                with open(filepath, 'wb') as f:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()
