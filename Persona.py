import pymongo


#mydict = { "_id": "1","name": "Peporro", "address": "lomejon" }
#x=mycol.insert_one(mydict)



class Persona:

    def __init__(self, _id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Persona"]
        query = {"_id": _id}
        mydoc = mycol.find_one(query)
        self._id = mydoc.get("_id")
        self.firstname = mydoc.get("firstname")
        self.lastname = mydoc.get("lastname")

    def __init__(self, _id, firstname, lastname):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Persona"]
        mydict = {"_id": _id, "firstname": firstname, "lastname": lastname}
        mycol.insert_one(mydict)
        self._id = _id
        self.firstname = firstname
        self.lastname = lastname

    def get_id(self):
        return self._id

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def delete(self):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["Persona"]
        query = {"_id": self._id}
        mycol.delete_one(query)
        self._id = None
        self.firstname = None
        self.lastname = None

    def __str__(self):
        return self._id + "; " + self.firstname + "; " + self.lastname

