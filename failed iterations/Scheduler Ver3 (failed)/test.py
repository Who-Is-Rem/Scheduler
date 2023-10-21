import pickle

with open("./information/customers.pickle", "rb+") as path:
    pickle.dump([], path)

with open("./information/employees.pickle", "rb+") as path:
    pickle.dump([], path)

with open("./information/services.pickle", "rb+") as path:
    pickle.dump([], path)