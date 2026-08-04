from importlib.metadata import version, PackageNotFoundError

name = "nba_api"
try:
    __version__ = version("nba_api")
except PackageNotFoundError:
    __version__ = "custom-local"