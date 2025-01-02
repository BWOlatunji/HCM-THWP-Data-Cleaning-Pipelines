import pandas as pd


def process_csv_file(
    input_file_path, output_file_path, parquet_output_file_path, columns_to_remove
):
    """
    This function imports a CSV file, removes specified columns, converts the birthdate column to MM/DD/YYYY format,
    adds a new column 'age' calculated from the birthdate, and saves the resulting DataFrame as a new CSV file.

    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to save the processed data as a CSV file.
    :param parquet_output_file_path: Path to save the processed data as a Parquet file.
    :param columns_to_remove: List of columns to be removed.
    """
    # Import the CSV file into a DataFrame
    df = pd.read_csv(
        input_file_path,
        skiprows=1,
        names=[
            "visitation_id",
            "patient_id",
            "patient_project_number",
            "patient_card_number",
            "facility_name",
            "start_date",
            "end_date",
            "time_in",
            "time_out",
            "created_at",
        ],
    )

    # Remove specified columns
    df = df.drop(columns=columns_to_remove)
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)
    df.to_parquet(parquet_output_file_path, compression="gzip")
    print(
        f"Processed Parquet and CSV files saved at: {output_file_path}, {parquet_output_file_path}"
    )


# Path to your input CSV file
input_file = "data/CureRite/visitations_export.csv"

# Path to save the output CSV file
output_file = "data/cleaned_data_files/visitations_cleaned.csv"
parquet_output_file_path = "data/cleaned_data_files/visitations_cleaned.parquet"
# Columns to remove from the data frame
columns_to_remove = [
    "patient_project_number",
    "patient_card_number",
    "created_at",
]

process_csv_file(
    input_file,
    output_file,
    parquet_output_file_path,
    columns_to_remove
)
