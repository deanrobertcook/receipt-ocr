import sys
import requests
import os
import json
import re

DEBUG = False
DB_PATH = 'cache/db.json'

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

BASE_URL = 'https://ocr.asprise.com/api/v1/receipt'  # Receipt OCR API endpoint

def cached_request_receipt_scan(filename):
  cache = os.path.join('cache', os.path.basename(filename) + ".json")

  if os.path.isfile(cache):
    if DEBUG:
      print(f"{cache} found, reading from file")
    with open(cache) as f:
      return (json.load(f), cache)
    
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
  return (js, cache)

receipts = sorted(os.listdir("receipts"), key=lambda f: os.path.getctime(os.path.join("receipts", f)))
# receipts = ['Double_20230304-1220.pdf']

pattern = r"^(.*(\d+[\,|\.]\d+).*)$"   
text_pattern = r"\D" # Match any non-digit character 

with open(DB_PATH) as f:
  db = json.load(f)

for i, f in enumerate(receipts):
  (js, cache) = cached_request_receipt_scan(os.path.join("receipts", f))
  if 'message' in js:
    print("Rate limit hit, stopping")
    os.remove(cache)
    exit(0)
  
  ocr_text = js['receipts'][0]['ocr_text']

  receipt = {
    "date": js['receipts'][0]['date'],
    "total": js['receipts'][0]['total'],
    "merchant": js['receipts'][0]['merchant_name'],
    "purchaser": f.split('_')[0],
    "file": f,
  }
  
  matches = re.findall(pattern, ocr_text, re.MULTILINE)

  items = []
  for match in matches:
    line_parts = match[0].strip().split("  ")
    is_text = lambda p: bool(re.search(text_pattern, p))
    item_name = list(filter(is_text, line_parts))[0].strip()

    price = match[1].strip()
    cents = int(price.replace(",", "").replace(".", ""))
    items.append([item_name, cents])

  receipt['items'] = items

  if f in db:
    if db[f]['items'] != receipt['items']:
      print("Items changed for", f, file=sys.stderr)
  else:
    db[f] = receipt
    with open(DB_PATH, 'w') as f:
      json.dump(db, f, indent=4, separators=(",", ": "))


  
