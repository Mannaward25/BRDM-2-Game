data: bytes
data = b''

with open('van.png', 'rb') as f:
    data = f.read()
    print(type(data))
    print(data)


with open('new.png', 'wb') as f:
    f.write(data)
