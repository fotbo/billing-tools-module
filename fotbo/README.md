# Fotbo module

## Endpoints vpn notyfication

### Create notification - HTTP method POST

```
https://bill.fotbo.host/backend/staffapi/fotbo/public/vpn-notification
```

Allowed params

```
:param ip_address: str (only for dev)
:vpn_user: str
:vpn_password: str
```
>* Return
>* HTTP status OK == 201_CREATED
>* HTTP status ERROR == 400_BAD_REQUEST
>* HTTP status ERROR == 404_NOT_FOUND


### Django config
```
# OVPN settings
VPN_ADMIN_APPUSER = APPUSER_ID
VPN_TICKET_DEPARTMENT = department_id

VPN_MESSAGE_TITLE = 'Login and Password for VPN Server'

VPN_MESSAGE_TEMPLATE = """"<b>VPN Server Details</b><br>
URL: https://{ip_user}<br>
User: {vpn_user}<br>
Password: {vpn_password}<br>"""
```