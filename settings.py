twilio_phonenumber = '+447897016821'
twilio_account_sid = b'QUM1NTJlYTRlNDUyOTc4YTQwYWQ4ZDAwNjFmYzgzZTA3Nw=='
twilio_auth_token = b'MjQ0ZTllMmJjNWQ1NTlmYmMxMjVlZjU4YTJlZGM3MGE='
consumer_key = b'TkpSMnBHU29pZVp5Ums5alRQQzR5cE85Wg=='
consumer_secret = b'TDJHZUR5R0d6TDBoZXpYUVFKNXNGODZnM25JbEQ3amc1RHNjZWJpU1dndGQ1YXlDMk4='
access_token = b'MTQ5NjU2NDc5Njk1MDUxOTgwOC1DTkdOTlgxZ2taUFNwcUFOeERVTDczbkZjclBrUU0='
access_token_secret = b'dllGTUtuZkhkQ0ZPR2g4YnVvVnRvTkozWXc2b0w5a09rN0dsMDl3VGhxaVlh'
imgflip_username = 'toilet.io'
imgflip_password = b'VG9pbGV0dGltZQ=='

#This header underpins the security of the program, everything is encrypted in base 64
#The actual decryption happens within function calls and thus nothing is exposed to the user directly
#Not even on the console itself, this enables a secure experience with API passwords thus not revealed.

def get_twilio_phonenumber():
    return twilio_phonenumber

def get_twilio_accountsid():
    return twilio_account_sid

def get_twilio_authtoken():
    return twilio_auth_token

def get_twitter_consumerkey():
    return consumer_key

def get_twitter_consumersecret():
    return consumer_secret

def get_twitter_accesstoken():
    return access_token

def get_twitter_accesstokensecret():
    return access_token_secret

def get_imgflip_username():
    return imgflip_username

def get_imgflip_password():
    return imgflip_password