from tmdb.tmdb_bulk_cleaner import TmdbBulkCleaner
from tmdb.tmdb_bulk_retriever import TmdbBulkRetriever
from tmdb.tmdb_data_retriever import TmdbDataRetriever
import os


class PlanningPrediction:
    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    # bulk_retriever = TmdbBulkRetriever(f"{os.path.dirname(__file__)}/data")
    # bulk_cleaner = TmdbBulkCleaner()
    data_retriever = TmdbDataRetriever()

    # bulk_data_path = bulk_retriever.retrieve_movies()
    
    # cleaned_data_path = bulk_cleaner.clean(bulk_data_path)

    cleaned_data_path=f"{os.path.dirname(__file__)}/data/2023-02-05.csv"

    data_retriever.retrieve(cleaned_data_path)
    
    # planning_prediction = PlanningPrediction()
