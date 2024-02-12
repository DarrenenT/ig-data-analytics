import csv

def split_csv(file_name, split_size):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        file_count = 0
        row_count = 0
        current_output_writer = None

        for row in csv_reader:
            if row_count % split_size == 0:
                if current_output_writer is not None:
                    output_file.close()

                output_file_name = f"{file_name.split('.')[0]}_{file_count}.csv"
                output_file = open(output_file_name, 'w', newline='')
                current_output_writer = csv.writer(output_file)
                current_output_writer.writerow(headers)
                file_count += 1

            current_output_writer.writerow(row)
            row_count += 1

        if current_output_writer is not None:
            output_file.close()

split_csv('target_accounts.csv', 20)  # replace with the path to your CSV file