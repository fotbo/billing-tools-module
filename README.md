# Staff firewall

A staff firewall is a security measure designed to manage instance traffic such as block/open SMTP port, block ingoing and outgoing traffic.
Firewall based on out of box features included into Arista and OPNsense devices

## Getting started

1) Clone and copy code to django project
2) Install required module
```bash
pip3 install -r requirements.txt
```
3) Enter to django shell mode and generate Fernet key
```bash
from cryptography.fernet import Fernet
print(Fernet.generate_key())
```
4) Open settings.py and add ENCRYPTION_KEY variable
```python
ENCRYPTION_KEY = YOUR_FERNER_KEY_HERE
```
5) Open settings.py and add app into INSTALLED_APPS
```python
INSTALLED_APPS += (
    'fleiostaff.tools.staff_firewall',
    )
```
6) Apply migrations
```python
python3 manege.py migrate
```
7) Now need to add firewall credentials. Go to admin page, find STAFF_FIREWALLS, open FwRegions and press "ADD" button

![img-1](https://github.com/fotbo/billing-tools-module/assets/124665380/21333f4d-13fa-438a-ad76-29212522a52c)

Example

![Screenshot](https://github.com/fotbo/billing-tools-module/assets/124665380/050d5628-4233-40ca-936a-3f6c379fc5b8)

> **_NOTE:_**  URL should be without slash.

