## Usage

#### Send free message to email, without your email!

```python
# Send free message to email, debug OFF
>>> from mail_server import *
>>> server.send("he1zen@null.net", "hello, its a test message!")
b'200'
>>>

# Send free message to email, debug ON
>>> from mail_server import *
>>> server.send("he1zen@null.net", "hello, its a test message!")
[3%] Debug mode ON
[7%] Using urllib3
[11%] Starting to get URL
[20%] Getting json from URL
[40%] URL json data decode
[60%] Server IP 18.189.106.45
[80%] Server connected!
[100%] Data send to server
b'200'
>>>

```
