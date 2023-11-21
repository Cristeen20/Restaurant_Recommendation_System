
import csv

def write_csv(data,csv_file):

    # Open the CSV file in write mode
    with open(csv_file, 'a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header row
        header = data[0].keys()
        csv_writer.writerow(header)

        # Write the data rows
        for row in data:
            try:
                csv_writer.writerow(row.values())
            except:
                continue