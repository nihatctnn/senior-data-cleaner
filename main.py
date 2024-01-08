import time
from src.DataPreprocessor import DataPreprocessor
from src.MongoConnector import MongoConnector
from src.utils import show_mode_status

# Display the status of the mode (edit and safe modes)
# show_mode_status()

# Create an instance of the DataPreprocessor class
dp = DataPreprocessor()

# Implement db to label mapping based to db on information from the label mapping file
# dp.implement_label_mapping()

time.sleep(2)
# Remove unused fields from the database for an artificial intelligence model
# dp.remove_unused_field()

# Convert the 'Year' fields to integers
dp.convert_to_integer()