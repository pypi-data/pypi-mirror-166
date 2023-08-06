"""Object for handling configuration."""
import json

class Config:

    """Configuration object."""

    def __init__(self):
        self._config = dict()


    def load(self, filepath, defaults_filepath=None):
        """Load configuration from a JSON filepath.

        Args:
            filepath (str): Path to the configuration file.
            defaults_filepath (str, optional): Path to the defaults (these are loaded first then overridden with filepath). Defaults to None.
        """

        _config = dict()

        # Load the defaults filepath if requested
        if defaults_filepath:
            _defaults = json.load(open(defaults_filepath, 'r')) 
            _config.update(_defaults)

        # Load the requested filepath and overlay
        _user = json.load(open(filepath, 'r'))
        _config.update(_user)

        # Set to the internal object.
        self._config = _config


    def get(self, key, default=None, cast=None):
        """Get the configuration value out of the configuration, with an optional default if it is not set.

        Args:
            key (str): Key (can be dot-recursive).
            default (mixed, optional): Default value if not found. Defaults to None (throws KeyError if not found).
            cast (callable, optional): Optionally recast the data into another type at runtime.
        
        Returns:
            mixed: Value returned by addressing key.

        Raises:
            KeyError: If there is no configutation option reachable from the key.
            Exception: If data cannot be recast.

        """
        candidate = None
        
        try:
            
            # Loop through each sub-key
            for _key in key.split('.'):

                if candidate is None:
                    candidate = self._config[_key]
                else:
                    candidate = candidate[_key]
        
        except KeyError:

            if default is not None:
                candidate = default
            
            else:
                raise KeyError(f'No reachable configuration option assigned to "{key}".')
        
        # Optional recasting
        if cast:
            return cast(candidate)
        
        # Return as is
        return candidate