import pickle


class Me:
    """info about me"""
    def __init__(self):
        self.name = "Pavel"
        self.surname = "Polushkin"
        self.age = 29
        self.height = 181
        self.weight = 85
        self.marital_status = True


obj = Me()


f = open('test.txt', 'wb')
pickle.dump(obj, f)

f.close()
