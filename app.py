import pymongo
import os,sys,json
from flask import jsonify,request,Flask

app = Flask(__name__)
def uri():
    url = os.getenv('mongo')
    print(f"la url es: {url}")
    return url
try:
  
  client = pymongo.MongoClient(uri())
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
#api
"""
@app.route('/create_database',methods=['POST'])
def create_database():
    data = request.get_json()
    collection = data.get('name_collection')
    name_db = data.get('name_db')
    try:
        print(f"la db es {name_db}")
        print(f"la coleccion es {collection}")
        if not name_db or not collection:
            return jsonify({"error": "Falta el nombre de la base de datos o de la coleccion."}), 400
        db = client[name_db]
        db[collection]
        return jsonify({
                "response" : f"La base de datos {name_db} fue creada con la coleccion {collection}"
        }),201
    except Exception as e:
        return jsonify({
            "error" : "Ocurrio algun problema",
            "message" : str(e)
        }),500
"""
@app.route('/get_databases',methods=['GET'])
def get_databases():
   try:
       print("entra al get")
       listDb = client.list_database_names()
       print(listDb)
       return jsonify({
           "response" : listDb
           
       }),200
   except Exception as e:
       return jsonify({
           "error" : "algo paso al tratar de acceder a las bases de datos",
           "message" : str(e)
       }),500

"""
@app.route("/create_collection",methods=['POST'])
def create_collection():
    data = request.get_json()
    collection = data.get('name_collection')
    name_db = data.get('name_db')
    try:
        if not name_db or not collection:
            return jsonify({"error": "Falta el nombre de la base de datos o de la coleccion."}), 400
        
        
        if name_db in client.list_database_names():
                db=client[name_db]
                db[collection]
                return jsonify({
                    "response" : f"coleccion {collection} creada con exito"
                }),201
    except Exception as e:
        return jsonify({
            "error":"Paso algo al tratar de crear el contenedor",
            "message": str(e)
        }),500
"""
@app.route('/get_collections',methods=['GET'])
def get_collections():
    data = request.get_json()
    name_db = data.get('name_db')
    try:
        if not name_db:
            return jsonify({
                "error" : "Debe enviar el nombre de la base de datos"
            }),400
        db = client[name_db]
        list_collecitons = db.list_collection_names()
        return jsonify({
            "response" : list_collecitons
        }),200
    except Exception as e:
        return jsonify({
            "error" : "No se pudo listar las colecciones",
            "message" : str(e)
        }),500
@app.route('/add_item',methods=['POST'])
def add_item():
    data = request.get_json()
    name_db = data.get('name_db')
    collection = data.get('name_collection')
    _id = data.get('_id')
    item = data.get('item')
    try:
        if not name_db or not collection or not item or not _id:
            return jsonify({
                "error" : "Debe enviar todos los datos necesarios",
                "message" : "los datos necesarios son: name_db,name_collection,item,_id",
                "note": "El _id es mejor que sea como el nombre de tu item, que este engloble una funcion especifica"
            }),400
        if verify_database(name_db=name_db):
            db = client[name_db]
            listCollections = db.list_collection_names()
            if collection in listCollections:
                col = db[collection]
                if search_id(id=_id,collection=col):
                    return jsonify({
                        "erro":"Ya existe un item con ese id"
                    }),409
                dta = {
                    "_id" : _id,
                    "item" : item
                }
                additem = col.insert_one(dta)
                return jsonify({
                    "response" : f"El item {item} fue ingresado con exito"
                }),201

            else:
                return jsonify({
                    "error" : f"La coleccion {collection} no existe dentro de la base de datos {name_db}"
                }),400

        else:
            return jsonify({
                "error" : f"La base de datos {name_db} mo existe"
            }),400


    except Exception as e:
        return jsonify({
            "error":"error al añadir el item",
            "message": str(e)

        }),500
    
@app.route('/delete_item',methods=['DELETE'])
def delete():
    data = request.get_json()
    name_db = data.get('name_db')
    collection = data.get('name_collection')
    _id = data.get('_id')
    
    try:
        if not name_db or not collection  or not _id:
                return jsonify({
                    "error" : "Debe enviar todos los datos necesarios",
                    "message" : "los datos necesarios son: name_db,name_collection,_id"
                }),400
        if verify_database(name_db=name_db):
            db = client[name_db]
            listCollections = db.list_collection_names()
            if collection in listCollections:
                col = db[collection]  
                if search_id(id=_id,collection=col):
                    response = col.delete_one({"_id": _id})
                    print(response)
                else:
                    return jsonify({
                        "response" : f"EL id {_id} no corresponde a ningun item"
                    }),404
                
                
                return jsonify({
                    "response" : f"El item {_id} fue eliminado con exito"
                }),201

            else:
                return jsonify({
                    "error" : f"La coleccion {collection} no existe dentro de la base de datos {name_db}"
                }),404

        else:
            return jsonify({
                "error" : f"La base de datos {name_db} mo existe"
            }),404
    except Exception as e:
        return jsonify({
            "error" : "ocurrio algo al tratar de eliminar el item",
            "message" : str(e)
        }),400
@app.route('/get_item',methods=['GET'])
def get_item():
    data = request.get_json()
    name_db = data.get('name_db')
    collection = data.get('name_collection')
    _id = data.get('_id')
    try:
        if not name_db or not collection  or not _id:
                return jsonify({
                    "error" : "Debe enviar todos los datos necesarios",
                    "message" : "los datos necesarios son: name_db,name_collection,_id"
                }),400
        if verify_database(name_db=name_db):
            db = client[name_db]
            listCollections = db.list_collection_names()
            if collection in listCollections:
                col = db[collection]
                it = search_id(collection=col,id=_id)
                if it:
                    return jsonify({
                        "response": it
                    }),200
                else:
                    return jsonify({
                        "error": f"El id {_id} no corresponde a ningun item"
                    }),404
            else:
                 return jsonify({
                    "error" : f"La coleccion {collection} no existe dentro de la base de datos {name_db}"
                }),404

        else:
            return jsonify({
                "error" : f"La base de datos {name_db} mo existe"
            }),404
    
    except Exception as e:
        return jsonify({
            "error" : "Acurrio algo al tratar de acceder a el item especifico",
            "message" : str(e)
        }),400
@app.route('/list_items')
def list_items():
    data = request.get_json()
    name_db = data.get('name_db')
    collection = data.get('name_collection')
    only_id = data.get('only_id')
    try:
        if not name_db or not collection or not only_id :
                    return jsonify({
                        "error" : "Debe enviar todos los datos necesarios",
                        "message" : "los datos necesarios son: name_db,name_collection,only_id"
                    }),400
        if verify_database(name_db=name_db):
             db = client[name_db]
             listCollections = db.list_collection_names()
             if collection in listCollections:
                 col = db[collection]
                 
                 cvtb = convert_to_boolean(dat=only_id)
                 if cvtb is None:
                     return jsonify({
                         "error" : "El perametro only_id tiene un valor erroneo",
                         "message" : "cambia su valor por 'yes' o 'none'"
                     })
                 if cvtb:
                     cole = col.find({},{"_id":1})
                     list_item = [str(doc["_id"]) for doc in cole]
                 else:     
                     cole = col.find()
                     list_item = [document for document in cole]    
                 return jsonify({
                         "response" : list_item
                     }),200
             else:
                    return jsonify({
                    "error" : f"La coleccion {collection} no existe dentro de la base de datos {name_db}"
                }),404


        else:
            return jsonify({
                "error" : f"La base de datos {name_db} mo existe"
            }),404

    except Exception as e:
        return jsonify({
            "error":"Ocurrio algo al tratar de acceder a los items"
            ,"message":str(e)
        }),500


#fuctions
def convert_to_boolean(dat):
    if dat in ['True','true','1','Yes','yes','y']:
        return True
    elif dat in ['False','false','0','None','none','n']:
        return False
    return None

   
def search_id(id,collection):
    item = collection.find_one({'_id':id})
    if item:
        return item
    return False
def verify_database(name_db):
    if name_db in client.list_database_names():
        return True
    return False




    


if __name__ == '__main__':
    app.run(debug=True,port=5001)
    





