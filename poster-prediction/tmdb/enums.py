from enum import Enum


class ExportType(Enum):
    """Represents the different data export types for TMDB

    Note that TMDB Data exports only provide ids and names of their DB items. 
    For the full data representation we need to hit the API using these ids.
    """
    MOVIE = "movie"
    TV = "tv_series"
    PEOPLE = "person"
    COLLECTION = "collection"
    NETWORK = "tv_network"
    KEYWORD = "keyword"
    COMPANY = "production_company"


class PosterSize(Enum):
    """Represents different poster sizes in TMDB
    """
    XTINY = "w92"
    TINY = "w154"
    XSMALL = "w185"
    SMALL = "w342"
    MEDIUM = "w500"
    LARGE = "w780"
    ORIGINAL = "original"
