import base64

def decode_string(string):
    decode_string = base64.b64encode(string.encode("UTF-8"))

    return decode_string.decode("UTF-8")

def encode_string(crypto_data):
    a = crypto_data.encode("UTF-8")
    return base64.b64decode(a)

crypto_data = decode_string("Привет Макс")

print(encode_string(crypto_data))
