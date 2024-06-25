# Staff firewall

A staff firewall is a security measure designed to manage instance traffic such as block/open SMTP port, block ingoing and outgoing traffic.
Firewall based on out of box features included into Arista and OPNsense devices
## Database designe

![Staff-firewall](https://github.com/fotbo/billing-tools-module/assets/124665380/0b89d728-f688-4ff3-8a63-e33c1431f30f)

## Endpoints
### Get create options - HTTP method GET

```
https://bill.fotbo.host/backend/staffapi/tools/firewall/create_options
```

###  Get list of firewall rules - HTTP method GET

```
https://bill.fotbo.host/backend/staffapi/tools/firewall
```
###  Add firewall rule - HTTP method POST
```
https://bill.fotbo.host/backend/staffapi/tools/firewall
```

Allowed params

```
:param action:
:param direction:
:param interface: [list]
:param protocol:
:param source_ip:
:param source_port:
:param destination_ip:
:param destination_port:
:param description:
:param enabled:
```
>* Return parsed filter rule
>* HTTP status OK == 201_CREATED
>* HTTP status ERROR == 400_BAD_REQUEST

Error example

```json
{
    "error": "{'non_field_errors': [ErrorDetail(string='This IP address is not allowed to be added to the firewall.', code='invalid')]}"
}
```

###  Update firewall rule - HTTP method PUT
```
https://bill.fotbo.host/backend/staffapi/tools/firewall/pk
```

Allowed params

```
:param action:
:param direction:
:param interface: [list]
:param protocol:
:param source_ip:
:param source_port:
:param destination_ip:
:param destination_port:
:param description:
:param enabled:
```
>* Return parsed filter rule
>* HTTP status OK == 201_CREATED
>* HTTP status ERROR == 400_BAD_REQUEST
>* HTTP status ERROR == 404_NOT_FOUND

###  Delete firewall rule - HTTP method DELETE
```
https://bill.fotbo.host/backend/staffapi/tools/firewall/pk
```
>* HTTP status OK == 204_NOT_CONTENT
>* HTTP status ERROR == 400_BAD_REQUEST
>* HTTP status ERROR == 404_NOT_FOUND

###  Disabled/Enabled rule
```
https://bill.fotbo.host/backend/staffapi/tools/firewall/pk/toggle_rule
```
>* HTTP status OK == 200.
>* HTTP status ERROR == 400_BAD_REQUEST.
>* HTTP status ERROR == 404_NOT_FOUND.

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
> **_NOTE:_**  URL should be without slash.

Example

![Screenshot](https://github.com/fotbo/billing-tools-module/assets/124665380/050d5628-4233-40ca-936a-3f6c379fc5b8)

### Extra settings
* **EXLUDED_PRIVATE_NETWORK:** - If you need allow to add IP from private network you can add that network here(type list).
* **RESERVED_NETWORK** - Reserved or system networks, those that cannot be blocked (type list).