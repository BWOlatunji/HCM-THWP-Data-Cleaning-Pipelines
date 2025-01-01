import os
import pandas as pd
import calendar


def process_excel_files(folder_path):
    all_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
            try:
                # Extract month and year from the file name
                file_parts = file_name.split()
                month = file_parts[-2]  # Extract the month
                year = file_parts[-1].replace(".xlsx", "")  # Extract the year

                # Convert month name to a number (e.g., Apr -> 4)
                month_number = pd.to_datetime(month, format="%b").month

                # Get the last day of the month using calendar.monthrange
                last_day = calendar.monthrange(int(year), month_number)[1]

                # Construct the date (YYYY-MM-DD)
                date = f"{year}-{month_number:02d}-{last_day:02d}"

                # Construct the full file path
                file_path = os.path.join(folder_path, file_name)

                # Read the Excel file into a DataFrame
                df = pd.read_excel(file_path, header=None)  # Read without assuming headers

                # Assign custom column names after reading (since header=None)
                df.columns = [
                    "s_no",
                    "psn",
                    "surname",
                    "other_names",
                    "grade_level",
                    "ministry",
                    "bank",
                    "account_no",
                    "basic_sal",
                    "allowances",
                    "gross",
                    "deduction",
                    "loans",
                    "tax",
                    "suspensions",
                    "net_pay",
                ]

                # Remove the first column, first 4 rows, and last 2 rows
                df = df.iloc[4:-2, 1:]

                # Add 'Month', 'Year', and 'Date' columns
                df["Month"] = month
                df["Year"] = year
                df["Date"] = date

                # Columns that are supposed to be numeric but might have commas
                numeric_columns = [
                    "basic_sal", "allowances", "gross", "deduction", "loans", "tax", "suspensions", "net_pay"
                ]

                # Remove commas from numeric columns, then convert to numeric
                for col in numeric_columns:
                    df[col] = df[col].str.replace(",", "").astype(float)

                # Append the cleaned DataFrame to the list
                all_data.append(df)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Concatenate all data frames into one
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    else:
        raise ValueError("No valid data found to process.")


# Folder path containing the Excel files
folder_path = "data/Payroll"

# Process the Excel files and combine them into one DataFrame
try:
    final_dataframe = process_excel_files(folder_path)

    # Save the combined data frame to a new Excel file
    final_dataframe.to_excel(
        "data/cleaned_data_files/combined_payroll_data.xlsx", index=False
    )

    # Save the combined DataFrame as a Parquet file
    final_dataframe.to_parquet(
        "data/cleaned_data_files/combined_payroll_data.parquet", compression="gzip"
    )

    print("Data saved successfully as Excel and Parquet files.")
except Exception as e:
    print(f"An error occurred: {e}")

# df=pd.read_parquet("data/cleaned_data_files/combined_payroll_data.parquet")
# print(df.head())