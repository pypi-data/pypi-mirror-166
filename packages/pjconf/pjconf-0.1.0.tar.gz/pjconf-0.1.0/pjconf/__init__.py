"""pjconf main module."""
from importlib.metadata import version
from pjconf.config import Config

# Version handle
__version__ = version('pjconf')


def load_config(filepath, defaults_filepath=None):
    """Shortcut to instantiate and load a configuration object.

    Args:
        filepath (str): Path to the user configuration.
        defaults_filepath (str, optional): Path to defaults filepath, overriden by filepath. Defaults to None.
    
    Returns:
        pjconf.config.Config : Configuration object
    """
    config = Config()
    config.load(filepath=filepath, defaults_filepath=defaults_filepath)
    return config