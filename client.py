import base64
import json
import requests

url = 'http://localhost:5000/notify_telegram'

image_file='get-into-iot.jpg'

info_cam = { #Creating dict for json format
            	"Camera ID": 1,
		        "Area di competenza": "monserrato",
                "Posizione": "Parco Vulcania",
                "Contenuto":"Spazzatura"
           }

with open(image_file,'rb') as f:
    im_bytes = f.read()
im_b64 = base64.b64encode(im_bytes).decode('utf8')

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

payload = json.dumps({"image": im_b64, "caption": info_cam})
response = requests.post(url,data=payload,headers=headers)
try:
    data=response.json()
    print(data)
except requests.exceptions.RequestException:
    print(response.text)
