import csv
import os

file_path = "data.csv"
header = ["MAC", "Serial", "Date", "Version"]

def ensure_file_exists():
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

def append_data(mac, serial, date, version):
    try:
        ensure_file_exists()
        
        # First, read any existing data
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, mode="r", newline="") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                existing_data = list(reader)
        
        # Write header and only the new row
        with open(file_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow([mac, serial, date, version])
        
        print(f"Successfully updated {file_path} with new record")
        
        # If we replaced an old record, print that info
        if existing_data:
            print(f"Previous record removed: {','.join(existing_data[-1])}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_last_record():
    try:
        ensure_file_exists()
        
        with open(file_path, mode="r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            rows = list(reader)
            
        if not rows:
            print(f"No data found in {file_path}")
            return None
            
        return rows[-1]  # Return the last row
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    current_data = get_last_record()
    if current_data:
        print(f"Current record: {','.join(current_data)}")