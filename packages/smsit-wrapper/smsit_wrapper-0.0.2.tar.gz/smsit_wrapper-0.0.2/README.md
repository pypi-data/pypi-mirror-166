# SMS-iT API Wrapper
> SMS-iT API Python wrapper 0.0.2

GitHub at: https://github.com/SMS-iT-ai/smsit_wrapper/blob/main/README.md
<br/>

## Table of Content 

- [Installation](#installation)
- [Requirements](#requirements)
- [Available Methods](#available-methods)
- [Example](#example)
- [Contribute](#contribute)

<br/>

### Installation
---
Available on [pypi](https://pypi.org/project/smsit_wrapper/)

```
pip install smsit_wrapper
```

<br/>

### Requirements
---
> Used runtime: Python 3.8

```
requests
```

<br/>

### Available methods
---

```
 'addAppointment', 'addContact', 'checkCredits', 'generateOTP', 'getContact', 'getContactByName', 'getGroupsList', 'sendMessageToContacts', 'sendMessageToGroup', 'validateOTP'

```


```python
from smsit_wrapper import smsit

h = smsit(token="MyToken", version="cloud") #version options : cloud or decentral
```

The official API Reference can be found [here](https://controlpanel.smsit.ai/users/api)

<br/>

### Example
---

To generate OTP:
```python
from smsit_wrapper import smsit

h = smsit(token="MyToken", version="cloud") #version options : cloud or decentral

print(h.generateOTP())

OUTPUT:
{'status': 'Success', 'msg': 'Otp Successfully Generated', 'otp': '94b87b'}

```

<br/>

### Contribute
---

Feel Free to contribute and expand the wrapper

<br/>

>To be updated
<br/>
Have Fun!
