from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import config
from src.utils import bcolors


class MongoConnector:

    def __init__(self, db_name=config.DATABASE_NAME, collection_name=config.COLLECTION_NAME,
                 client_adr=config.CLIENT_ADR):
        """
                Creates an instance of MongoConnector with the necessary information for MongoDB connection.

                Args:
                    db_name (str): Database name.
                    collection_name (str): Collection name.
                    client_address (str): MongoDB server address.

                Attributes:
                    db_name (str): Stores the database name.
                    collection_name (str): Stores the collection name.
                    client_address (str): Stores the MongoDB server address.
                    collection: Stores the collection object.
                    db: Stores the database object.
                    client: Stores the MongoClient object.
                """
        self.db_name = db_name
        self.collection_name = collection_name
        self.client_address = client_adr

        self.collection = None
        self.db = None
        self.client = None

    def start_connection(self):
        """
                Establishes a connection with the MongoDB server and updates the database and collection objects.

                Returns:
                    None
                """
        self.client = MongoClient(self.client_address)  # MongoDB bağlantısı kur
        self.db = self.client[self.db_name]  # Veritabanı adını güncelle
        self.collection = self.db[self.collection_name]  # Koleksiyon adını güncelle
        print(bcolors.OKBLUE, "[OK] MONGO CONNECTION OK")

    def get_unique_values(self, column_name):
        """
               Retrieves unique values from a specific column.

               Args:
                   column_name (str): The name of the column from which to retrieve unique values.

               Returns:
                   list: A list containing unique values from the specified column.
               """
        return self.collection.distinct(column_name)

    def update_documents_by_model(self, model, model_value, new_field_value):
        """
                Updates documents with a specific model and value.

                Args:
                    model (str): The model name used to filter documents to be updated.
                    model_value: (str): The model value used to filter documents to be updated.
                    new_field_value: (str): The new field value to be added or updated in the documents.

                Returns:
                    None
                """
        # Define a query to filter documents based on the specified model and value.
        query = {model: model_value}
        # Define update data to set the new field value in the documents.
        update_data = {"$set": {model: new_field_value}}
        # Perform the update operation on multiple documents that match the query.
        result = self.collection.update_many(query, update_data)

        # Check if the update operation was successful or ignored based on configuration.
        if not config.DB_ERROR_IGNORE and result.modified_count <= 0:
            # Print an error message if the document was not updated or an error occurred.
            print(bcolors.FAIL, f"[ERROR] The document was not updated or an error occurred. {model}:{model_value}")

    def remove_field(self, field_to_remove):
        """
            Removes the specified field from the MongoDB collection.

            Args:
                field_to_remove (str): The name of the field to be removed.

            Returns:
                None
            """
        # Use the $unset operator to remove the field from the collection
        result = self.collection.update_many({}, {"$unset": {field_to_remove: 1}})

        # If the operation is successful
        if not config.DB_ERROR_IGNORE and result.modified_count <= 0:
            print(bcolors.FAIL, f"[ERROR] field not removed or not found. field:{field_to_remove}")

    def create_copy_collection(self, source_collection_name=config.COLLECTION_NAME, ):
        print(bcolors.OKCYAN, f"[START] STARTING TO CREATE A COPY OF COLLECTION")

        destination_collection_name = source_collection_name + '_copy'

        source_collection = self.db[source_collection_name]
        data_to_copy = source_collection.find()

        destination_collection = self.db[destination_collection_name]
        try:
            destination_collection.insert_many(data_to_copy)
        except BulkWriteError:
            print(bcolors.FAIL,
                  f"[ERROR] CAN NOT COPY TO COLLECTION. S:{source_collection_name} D:{destination_collection_name}")
            return False
        else:
            print(bcolors.OKGREEN,
                  F"[FINISH] SUCCESSFULLY COPIED S:{source_collection_name} D: {destination_collection_name}")
            return True
