import pymongo

print("Hello world!")
print("elDavi")
print("elAdri")
print("laMaria")
print("elBrayano")
print("prueba")
print("adri intenta subirlo bien")

client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net/Gestiondb?retryWrites=true&w=majority")
mydb = client["Gestiondb"]
mycol = mydb["ejemplo"]
mydict = { "_id": "1","name": "Peporro", "address": "lomejon" }
#x=mycol.insert_one(mydict)
query = {"_id": "1"}
mydoc=mycol.find(query)
for x in mydoc:
    print(x)