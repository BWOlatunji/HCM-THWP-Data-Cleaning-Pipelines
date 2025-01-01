import os
import pandas as pd
import calendar


def process_excel_files(folder_path):
    all_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
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
            df = pd.read_excel(
                file_path,
                names=[
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
                ],
            )

            # Remove the first column, first 4 rows, and last 2 rows
            df = df.iloc[4:-2, 1:]

            # Add 'Month', 'Year', and 'Date' columns
            df["Month"] = month
            df["Year"] = year
            df["Date"] = date

            # Append the cleaned DataFrame to the list
            all_data.append(df)

    # Concatenate all data frames into one
    combined_df = pd.concat(all_data, ignore_index=True)

    return combined_df


folder_path = "data/Payroll"
final_dataframe = process_excel_files(folder_path)

# Save the combined data frame to a new Excel file
final_dataframe.to_excel(
    "data/cleaned_data_files/combined_payroll_data.xlsx", index=False
)
