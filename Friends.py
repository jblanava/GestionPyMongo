import pymongo

from People import People


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

        query = {"_id1": _id1, "_id2": _id2}
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
        query = {"_id1": self._id1, "_id2": self._id2}
        mycol.delete_one(query)
        self._id1 = None
        self._id2 = None


