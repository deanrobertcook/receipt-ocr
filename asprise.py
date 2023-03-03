import requests
import os
import json

DEBUG = True

BASE_URL = 'https://ocr.asprise.com/api/v1/receipt'  # Receipt OCR API endpoint
# // Modify this to use your own file if necessary
imageFile = "/Users/deancook/Meine Ablage/receipt-scanner/230223-BC.pdf"


def cached_request_receipt_scan(filename):
  cache = os.path.join('cache', os.path.basename(filename) + ".json")
  if os.path.isfile(cache):
    if DEBUG:
      print(f"{cache} found, reading from file")
    with open(cache) as f:
      return json.load(f)
  if DEBUG:
    print(f"{cache} not found, fetching")
  response = requests.post(
      BASE_URL,
      data={
          'api_key': 'TEST',        # Use 'TEST' for testing purpose \
          'recognizer': 'DE',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
      },
      files={"file": open(filename, "rb")})

  js = json.loads(response.text)
  os.makedirs(os.path.dirname(cache), exist_ok=True)
  with open(cache, 'w') as f:
    json.dump(js, f, indent=4, separators=(",", ": "))
  return js


for f in os.listdir("receipts"):
  cached_request_receipt_scan('receipts/' + f)
