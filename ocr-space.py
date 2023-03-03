import requests
import base64

# Replace with your API key and endpoint URL
api_key = 'K86579300988957'
endpoint_url = 'https://api.ocr.space/parse/image'

# Read image file and encode as base64
with open('test-receipt4.jpeg', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
    img_data = 'data:image/jpeg;base64,' + img_data

# Send API request and get response
response = requests.post(endpoint_url, data={
    'apikey': api_key,
    'base64Image': img_data,
    'language': 'ger',
    'isTable': True,
})

print(response.json())

# Print OCR results
if response.status_code == 200:
    for result in response.json()['ParsedResults']:
        print(result['ParsedText'])
else:
    print('Error:', response.json()['ErrorMessage'])
