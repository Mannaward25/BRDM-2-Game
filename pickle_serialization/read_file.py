import pickle
from main import Me


f = open('test.txt', 'rb')
data: Me = pickle.load(f)
print(data.name, data.surname)

f.close()