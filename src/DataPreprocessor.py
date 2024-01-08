import config
from tqdm import tqdm

from src import utils
from src.DataFinder import DataFinder
from src.MongoConnector import MongoConnector
from src.utils import bcolors, is_edit_mode_active


class DataPreprocessor:
    """
        The DataPreprocessor class handles the preprocessing tasks for updating and modifying data in a MongoDB database.

        It includes methods to implement label mapping based on a label mapping file, remove unnecessary fields
        from the database for an artificial intelligence model, and create a label mapping from attribute configurations.
        The class ensures that edit and safe modes are active before performing operations, and communicates with
        the DataFinder and MongoConnector classes for data retrieval and database updates.

        Attributes:
            dataFinder (DataFinder): An instance of the DataFinder class for retrieving data from JSON files.
            mongo_conn (MongoConnector): An instance of the MongoConnector class for MongoDB database operations.

        Methods:
            - implement_label_mapping(): Updates the database based on the information from the label mapping file.
            - remove_unused_field(): Removes unnecessary fields from the database for an artificial intelligence model.
            - create_label_map(): Creates a label mapping based on the information from the attribute configuration file
        """

    def __init__(self):
        self.dataFinder = DataFinder();
        self.mongo_conn = MongoConnector()

        self.mongo_conn.start_connection()



    def implement_label_mapping(self):
        """
            Updates the database based on the information from the label mapping file.

            This function first checks if the edit mode is active before proceeding with the database update.
            It retrieves data from the label mapping file using the dataFinder, and if successful,
            it iterates through the data to update the corresponding documents in the database.

            Returns:
                bool: True if the update is successful, False otherwise.
            """
        print(bcolors.OKCYAN, f"[START] STARTING LABEL MAP IMPLEMENTATION")

        if not is_edit_mode_active():
            # If edit mode is not active, exit the function.
            return False

        # Retrieve data from the label mapping file.
        data = self.dataFinder.get_data_from_json(file_path=config.LABEL_MAPPING_PATH)
        if data is not None:
            # If data is successfully retrieved, proceed with the database update.
            print(bcolors.OKBLUE, "[OK] LABEL MAP FOUNDED")
            for model_name in tqdm(data.keys(), desc="Processing", unit="modul"):
                for model_value in data[model_name].keys():
                    # Update the database documents based on the label mapping information.
                    self.mongo_conn.update_documents_by_model(model=model_name, model_value=model_value,
                                                              new_field_value=data[model_name][model_value])
            print(bcolors.OKGREEN, "[FINISH] DB ADAPTED TO LABEL MAPPING")
            return True
        else:
            # If data retrieval fails, print an error message and exit the function.
            print(bcolors.FAIL, "[FAIL] FAIL TO ADAPTING LABEL MAPPING")
            return False

    def remove_unused_field(self):
        """
            Function to remove unnecessary fields from the database for an artificial intelligence model.

            Returns:
                bool: Indicates whether the operation was successful or not.
            """

        print(bcolors.OKCYAN, f"[START] STARTING TO DELETE FIELD")

        if not is_edit_mode_active():
            # If edit mode is not active, exit the function.
            return False

        # Retrieve data from the file config path.
        field_configs = self.dataFinder.get_data_from_json(file_path=config.FIELD_CONFIG_PATH)
        if field_configs is not None:
            print(bcolors.OKBLUE, "[OK] FIELD_CONFIG_PATH FOUNDED")

            # Check each field in the label mapping file
            for field_name in tqdm(field_configs.keys(), desc="Processing", unit="field"):
                # Remove fields specified with "DELETE" operation
                if field_configs[field_name]["operation"] == "DELETE":
                    self.mongo_conn.remove_field(field_to_remove=field_name)

            print(bcolors.OKGREEN, "[FINISH] DELETED FIELD")
            return True
        else:
            print(bcolors.FAIL, "[FAIL] FAIL TO DELETE FIELD")
            return False

    def create_label_map(self):
        """
            Creates a label mapping based on the information from the attribute configuration file.

            This function retrieves data from the 'attribute_config.json' file using the dataFinder.
            It checks if safe mode is not active and if the label mapping file doesn't already exist.
            If conditions are met, it iterates through the attributes, and for those marked with
            'LABEL_ENCODE' operation, it retrieves unique values from the corresponding database column.
            It then creates a label mapping dictionary with initial numerical values, and writes
            the resulting label mapping to a 'label_mapping.json' file.

            Returns:
                bool: True if the label map is successfully created, False otherwise.
            """
        data = self.dataFinder.get_data_from_json(file_path=config.FIELD_CONFIG_PATH)
        dictionary = {}
        # Check if safe mode is not active and the label mapping file doesn't exist.
        if not utils.is_safe_mode_active() and not self.dataFinder.is_file_exist(file_path=config.LABEL_MAPPING_PATH):

            data_attributes_names = data.keys()

            for column_name in tqdm(data_attributes_names, desc="Processing", unit="modul"):

                # Check if the operation is 'LABEL_ENCODE'.
                if data[column_name]["operation"] == "LABEL_ENCODE":
                    # Retrieve unique values from the corresponding database column.
                    db_data = self.mongo_conn.get_unique_values(column_name=column_name)
                    data_initial_num = int(data[column_name]["initial_num"])

                    # Create a label mapping dictionary with initial numerical values.
                    dictionary[column_name] = {marka: index + data_initial_num for index, marka in enumerate(db_data)}

            # Write the label mapping to a JSON file.
            self.dataFinder.write_to_json(file_path=config.LABEL_MAPPING_PATH, data=dictionary)
            print(bcolors.OKGREEN, "[FINISH] LABEL MAP IS CREATED")
        else:
            # If conditions are not met, print an error message and exit the function.
            print(bcolors.FAIL, "[FAIL] FAIL TO CREATING LABEL MAP")
            return False

    def convert_to_integer(self):

        """
        Converts the values of the "Yıl" field in a MongoDB collection to integers.

        - Prints a start message for the integer conversion process.
        - Checks if edit mode is active; if not, exits with False.
        - Retrieves data from MongoDB using get_data.
        - Iterates through each document, extracting "Yıl" field values.
        - Attempts to convert non-None string values to integers.
        - Updates MongoDB collection with successful conversions.
        - Prints a completion message for the conversion process.
        - Returns True if successful, False if data retrieval fails.
        """

        print(bcolors.OKCYAN, f"[START] STARTING INTEGER CONVERSION")

        # Check if the edit mode is active using a function is_edit_mode_active()
        if not is_edit_mode_active():
            return False

        # Retrieve data from the MongoDB collection using the get_data method
        result = self.mongo_conn.fetch_all_years()

        # Check if the retrieved result is not None before iterating
        if result is not None:

            # Iterate through each document in the result
            for document in tqdm(result, desc="Processing", unit="field"):
                # Get the value of the field "Yıl" from the current document
                year_value = document.get("Yıl")

                # Check if the year_value is not None
                if year_value is not None:
                    data_type = type(year_value)

                    # If the data type is a string, perform the conversion to an integer
                    if data_type == str:
                        # Remove double quotes from the string
                        year_value = year_value.strip('"')

                        try:
                            # Attempt to convert the year value to an integer
                            year_value_as_int = int(year_value)

                            # Update the MongoDB collection with the new integer value
                            self.mongo_conn.update_documents_by_model(model="Yıl", model_value=year_value,
                                                                      new_field_value=year_value_as_int)

                        except ValueError:
                            # Handle the case when the conversion to an integer fails
                            print(f"Error: The value '{year_value}' could not be converted to an integer.")

            print(bcolors.OKGREEN, "[FINISH] INTEGER CONVERSION COMPLETE")
            return True
        else:
            # Handle the case when the result from the MongoDB query is None
            print(bcolors.FAIL, "[FAIL] FAILED TO RETRIEVE DATA")
            return False