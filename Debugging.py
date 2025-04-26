import os
import pickle


class Debugging:
    def __init__(self, debug: bool = False):
        self.debug = debug

        if self.debug:
            # Ensure the debug directory exists
            if not os.path.isdir("./debug"):
                os.mkdir("./debug")

    def debug_print(self, message: str):
        """Print debug messages if debug is enabled."""
        if self.debug:
            print(message)

    def debug_store(self, data: any, file_name: str):
        """Store data in a pickle file if debug is enabled."""
        if self.debug:
            file_name += ".pkl"
            with open(file_name, 'wb') as file:
                pickle.dump(data, file)