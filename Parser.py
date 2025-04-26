import argparse

class Parser:
    def __init__(self, input_file: str):
        """
        Initializes the Parser class, which handles both file and command-line argument parsing.

        Args:
            input_file (str): The name of the input file to parse.
        """
        self.input_file = input_file
        self.config = self.parse_input_file(input_file)  # Parse the file immediately
        self.args = self.parse_command_line_args()       # Parse command-line arguments

    def parse_input_file(self, file_name: str) -> dict:
        """
        Parses a configuration file for key-value pairs and stores them in a dictionary.

        Args:
            file_name (str): The name of the input file to parse.

        Returns:
            dict: A dictionary with parsed key-value pairs.
        """
        data = {}

        try:
            with open(file_name, 'r') as file:
                for line in file:
                    # Strip leading/trailing whitespace
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue

                    # Split key and value by '='
                    if '=' in line:
                        key, value = line.split('=', 1)  # Split at the first '='
                        key = key.strip()
                        value = value.strip()

                        # Attempt to infer the value type (int, float, str)
                        if value.isdigit():
                            value = int(value)  # Convert to int
                        else:
                            try:
                                value = float(value)  # Convert to float
                            except ValueError:
                                pass  # Keep as string if neither int nor float

                        # Store the parsed key-value pair
                        data[key] = value
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' does not exist.")
        except Exception as e:
            print(f"Error while parsing the file: {e}")

        return data

    def parse_command_line_args(self):
        """
        Parses command-line arguments using argparse.

        Returns:
            argparse.Namespace: The parsed arguments.
        """
        parser = argparse.ArgumentParser(description="Parser for command-line arguments and configuration files")
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        return parser.parse_args()

    def get_config_value(self, key, default=None):
        """
        Gets a configuration value from the parsed input file.

        Args:
            key (str): The configuration key to retrieve.
            default (any): The default value if the key is not found.

        Returns:
            any: The value associated with the key, or the default value.
        """
        
        return self.config.get(key, default)
