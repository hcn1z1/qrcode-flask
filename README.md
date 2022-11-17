# CCNA QrCode

## requirements
technology used is python 3.7.x and Javascript. All external required libraries are noted on **requirements.txt**.

## Qrcode generator
this program is used to generate a qr code from **JSON file** of registered members.. it will send also email to them

```
{
    "members":[
        {"name":"first member",
        "lastname":"lastname first member",
        "email":"first member's email
        }
    ]
}
```
```
from createQr import *
initThread(filepath)
```

## QrCode Scanner
this webapp can be used to check if a qr code is valid.
### Steps
run python program: 

```python scanQr.py```

this will host locally and on network as well ! NOTE: it will be an https server becuz **getUserMedia** method presented by JS will not work unless of secure connection.

next step is accessing the https://ipv4:port from your phone.
