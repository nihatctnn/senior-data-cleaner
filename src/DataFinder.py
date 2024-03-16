import json
from src.utils import bcolors


class DataFinder:

    def __init__(self):
        pass

    def get_data_from_json(self, file_path):
        """
                Reads data from a JSON file.

                Args:
                    file_path (str): The path to the JSON file.

                Returns:
                    dict: The loaded data as a dictionary.
                    None: If the file is not found or an error occurs during loading.
                """
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                print(bcolors.OKCYAN, f"[INFO] FILE IS EXIST path:{file_path}")
                return json.load(file)
        except FileNotFoundError:
            print(bcolors.FAIL, f"[ERROR] FILE NOT FOUND path:{file_path}")
            return None

    def write_to_json(self, file_path, data):
        """
                Writes data to a JSON file.

                Args:
                    file_path (str): The path to the JSON file.
                    data (dict): The data to be written.

                Returns:
                    None
                """
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=3, ensure_ascii=False)

    def is_file_exist(self, file_path):
        """
                Checks if a file exists.

                Args:
                    file_path (str): The path to the file.

                Returns:
                    bool: True if the file exists, False otherwise.
                """
        try:
            file = open(file_path, "r")
        except FileNotFoundError:
            print(bcolors.OKCYAN, f"[INFO] FILE IS NOT EXIST path:{file_path}")
            return False
        else:
            print(bcolors.OKCYAN, f"[INFO] FILE IS EXIST path:{file_path}")
            return True