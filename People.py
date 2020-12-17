import pymongo


class People:

    @staticmethod
    def lista_amigos(_id):
        conjunto = Friends.conjunto_amigos(_id)
        lista = list(conjunto)
        lista.sort()
        return lista

    @staticmethod
    def lista_disponibles(_id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]
        mydoc = mycol.find()
        conjunto = set()

        for x in mydoc:
            index = x.get("_id")
            if index != _id:
                person = People(index)
                conjunto.add(person)

        conjuntoamigos = Friends.conjunto_amigos(_id)
        conjuntodis = conjunto.difference(conjuntoamigos)



        #Quitamos a la misma persona

        listadispo = list(conjuntodis)
        listadispo.sort()
        return listadispo

    def __init__(self, _id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]

        query = {"_id": _id}
        mydoc = mycol.find_one(query)
        self._id = mydoc.get("_id")
        self.firstname = mydoc.get("firstname")
        self.lastname = mydoc.get("lastname")

    def get_id(self):
        return self._id

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def __str__(self):
        return str(self._id) + "; " + self.firstname + "; " + self.lastname

    def __lt__(self, other):
        return self.get_id() < other.get_id()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return self.get_id()


class Friends:

    @staticmethod
    def conjunto_amigos(_id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Friends"]
        query = {"$or": [{"_id1": _id}, {"_id2": _id}]}
        mydoc = mycol.find(query)
        res = set()

        for x in mydoc:
            if x.get("_id1") == _id:
                p = People(x.get("_id2"))
                res.add(p)
            else:
                p = People(x.get("_id1"))
                res.add(p)

        return res

    def __init__(self, _id1, _id2):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Friends"]

        query = {"$or": [{"_id1": _id1, "_id2": _id2}, {"_id1": _id2, "_id2": _id1}]}
        mydoc = mycol.find_one(query)

        if mydoc is None:
            mydict = {"_id1": _id1, "_id2": _id2}
            mycol.insert_one(mydict)
            self._id1 = _id1
            self._id2 = _id2
        else:
            self._id1 = mydoc.get("_id1")
            self._id2 = mydoc.get("_id2")

    def get_id1(self):
        return self._id1

    def get_id2(self):
        return self._id2

    def delete(self):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Friends"]
        query = {"$or": [{"_id1": self._id1, "_id2": self._id2}, {"_id1": self._id2, "_id2": self._id1}]}
        mycol.delete_one(query)
        self._id1 = None
        self._id2 = None


amigos1 = People.lista_amigos(1)
print("Panas: ")
for x in amigos1:
    print(x)

print("Now disp: ")
disp1 = People.lista_disponibles(1)
for x in disp1:
    print(x)


