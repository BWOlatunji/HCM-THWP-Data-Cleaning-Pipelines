import pandas as pd
from datetime import datetime

# date_str = '09-19-2022'

# date_object = datetime.strptime(date_str, '%m-%d-%Y').date()


def process_csv_file(
    input_file_path, output_file_path, columns_to_remove, birthdate_column
):
    """
    This function imports a CSV file, removes specified columns, converts the birthdate column to MM/DD/YYYY format,
    adds a new column 'age' calculated from the birthdate, and saves the resulting DataFrame as a new CSV file.

    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to save the processed CSV file.
    :param columns_to_remove: List of columns to be removed.
    :param birthdate_column: The name of the birthdate column to convert and calculate age from.
    """
    # Import the CSV file into a DataFrame
    df = pd.read_csv(
        input_file_path,
        names=[
            "patient_id",
            "patient_project_number",
            "patient_card_number",
            "gender",
            "marital_status",
            "birthdate",
            "state_name",
            "lga_name",
            "ward_name",
            "town_name",
            "facility_name",
            "created_at",
        ],
    )

    # Remove specified columns
    df = df.drop(columns=columns_to_remove)

    # Convert the birthdate column to datetime and format it as MM/DD/YYYY
    df[birthdate_column] = pd.to_datetime(
        df[birthdate_column], format="%d/%m/%Y", errors="coerce"
    )
    df[birthdate_column] = df[birthdate_column].dt.strftime("%m/%d/%Y")

    # Create a new 'age' column
    current_date = datetime.now()  # Get the current date
    df["age"] = pd.to_datetime(df[birthdate_column], format="%m/%d/%Y").apply(
        lambda birthdate: current_date.year
        - birthdate.year
        - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    )

    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Processed CSV file saved at: {output_file_path}")


# Path to your input CSV file
input_file = "data/CureRite/patients_export.csv"

# Path to save the output CSV file
output_file = "data/cleaned_data_files/patients_cleaned.csv"
# Columns to remove from the data frame
columns_to_remove = [
    "patient_project_number",
    "patient_card_number",
    "created_at",
]
# Name of the birthdate column
birthdate_column = "birthdate"

process_csv_file(input_file, output_file, columns_to_remove, birthdate_column)
