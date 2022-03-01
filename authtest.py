import base64

import settings
import hashlib

passw = settings.get_imgflip_password()
new = base64.b64decode(passw).decode("utf-8")
print(passw)
print(new)