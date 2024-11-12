# Function to find and display duplicate primary_keys with filtering
def find_duplicate_primary_keys(sheets_service, spreadsheet_id, range_name, primary_key_col_name, filter_col_name, filter_value):
    # Finds and prints all duplicate primary_keys where filter_col_name equals filter_value.
    try:
        # Define the range to fetch (from row 3 onwards)
        range_to_fetch = f"{range_name}!A3:ZZZ"

        # Get values from the worksheet starting from row 3
        worksheet = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_to_fetch
        ).execute()
        data = worksheet.get('values', [])
        if not data:
            print(f"The {range_name} worksheet is empty.")
            return

        # Extract the header row (from data[0], which corresponds to row 3)
        header = data[0]

        # Find the index of the primary_key column (case-insensitive)
        try:
            primary_key_col_index = next(
                i for i, col_name in enumerate(header)
                if col_name.strip().lower() == primary_key_col_name.strip().lower()
            )
        except StopIteration:
            raise Exception(f"Column '{primary_key_col_name}' not found in the header.")

        # Find the index of the filter_col_name (case-insensitive)
        try:
            filter_col_index = next(
                i for i, col_name in enumerate(header)
                if col_name.strip().lower() == filter_col_name.strip().lower()
            )
        except StopIteration:
            raise Exception(f"Column '{filter_col_name}' not found in the header.")

        # Ensure there are enough rows to start from row 5
        if len(data) < 3:
            print("Not enough data to process.")
            return

        # Extract primary_keys where filter_col_name equals filter_value (starting from data[2], which corresponds to row 5)
        primary_keys = [
            row[primary_key_col_index]
            for row in data[2:]  # data[2] corresponds to row 5
            if len(row) > max(primary_key_col_index, filter_col_index)
               and row[filter_col_index].strip() == filter_value
               and row[primary_key_col_index]
        ]

        # Count occurrences of each primary_key
        primary_key_counts = Counter(primary_keys)

        # Find duplicates (primary_keys with a count greater than 1)
        duplicates = {primary_key: count for primary_key, count in primary_key_counts.items() if count > 1}

        if duplicates:
            print("Duplicate primary_keys found:\n")
            for primary_key, count in duplicates.items():
                print(f"Primary key: '{primary_key}', Found: {count} times")
        else:
            print("No duplicate primary_keys found.")

        return data, header, primary_keys, duplicates

    except Exception as e:
        raise Exception(f"Error finding duplicate primary_keys: {e}")