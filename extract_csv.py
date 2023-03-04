import json
import csv

DB_PATH = 'cache/db.json'

with open(DB_PATH) as f:
  db = json.load(f)

flattened = []
for k, v in db.items():
  for item in v['items']:
    flattened.append({
      "date": v['date'],
      "item": item[0],
      "price": item[1],
      "file": v['file'],
    })

header = ["date", "item", "price", "file"]

# Define the filename for the CSV file
filename = "my_objects.csv"

# Open the CSV file for writing
with open(filename, 'w', newline='') as csvfile:

    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=header)

    # Write the header row to the CSV file
    writer.writeheader()

    # Write each object to a row in the CSV file
    for obj in flattened:
        writer.writerow(obj)
