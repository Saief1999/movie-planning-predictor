import os


class SecretsManager:
    @staticmethod
    def retrieve_api_key(env_variable_name: str = "TMDB_API_KEY") -> str:
        """Retrieves TMDB Api Key from env

        Args:
            env_variable_name (str, optional): the environment variable name. Defaults to "TMDB_API_KEY".

        Raises:
            Exception

        Returns:
            str: the API KEY
        """
        api_key = os.getenv(env_variable_name)
        if api_key is None:
            raise Exception(
                f"API Key Not found. Please set env variable '{env_variable_name}'")
        return api_key
