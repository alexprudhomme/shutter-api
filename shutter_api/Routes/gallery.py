from flask import request, jsonify
import uuid
from datetime import datetime
from shutter_api.MySQL_command import *

class GalleryError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def gallery(app) -> None:
    
    @app.route("/gallerys", methods=["Post"])
    def post_gallerys():
        data = request.get_json()
        try:
            username = data["username"]
            description = data["description"]
            private = data["private"]
            
            if username == "":
                raise GalleryError("username param invalid")
            if description == "":
                raise GalleryError("description param invalid")
            if type(private) is not bool:
                raise GalleryError("private is not bool")
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "gallery_id": uuid.uuid4(),
            "description":description,
            "private":int(private),
            "creator_username": username,
            "created_date": datetime.utcnow().isoformat()
        }
        
        if createGallery(data):
            return jsonify({"gallery_id": data["gallery_id"]}), 201
        else:
            return jsonify({"creation status": "Fail"}), 400
        
    
    @app.route("/gallerys/<gallery_id>", methods=["Post"])
    def post_gallerys_galleryId(gallery_id):
        data = request.get_json()
        try:
            publication_id = data["publication_id"]
            
            if publication_id == "":
                raise GalleryError("publication_id param invalid")
            
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "publication_id": publication_id,
            "gallery_id": gallery_id
        }
        getAllSave()
        if addPublicationToGallery(data):
            return "ok", 201
        else:
            return jsonify({"adding status": "Fail"}), 400
        

    
    @app.route("/gallerys/<gallery_id>/like", methods=["Post"])
    def post_gallerys_galleryId_like(gallery_id):
        data = request.get_json()
        try:
            rating = data["rating"]
            username = data["username"]
            if type(rating) is not bool:
                raise GalleryError("like is not of boolean type")
            if username == "":
                raise GalleryError("username param invalid")
        except KeyError:
            return jsonify({'error': "missing json param"}), 400
        except GalleryError as e:
            return jsonify({'error': e.args[0]}), 400
        
        data = {
            "rating": int(rating),
            "gallery_id": gallery_id,
            "username": username
        }
        
        if likeGallery(data):
            getAllRateGallery()
            return jsonify({"status": "succes"}), 200
        else:
            return jsonify({"status": "Fail"}), 400
        
    @app.route("/gallerys/<gallery_id>", methods=["DELETE"])
    def delete_gallerys_galleryId(gallery_id):

        
        if deleteGalleryFromDB(gallery_id):
            getAllGallery()
            return jsonify({"deleted status": "succes"}),200
        else:
            return jsonify({"deleted status": "fail"}),400
    
    
    @app.route("/gallerys/<gallery_id>", methods=["GET"])
    def get_gallerys_galleryId(gallery_id):
        
        data = getGalleryById(gallery_id)
        if data is None:
            return jsonify({"Error": "gallery_id does not exist"}),400
        else:
            return jsonify(data),200