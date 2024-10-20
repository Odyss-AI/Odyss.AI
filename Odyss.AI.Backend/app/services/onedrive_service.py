import os
import logging
import gridfs
from bson.objectid import ObjectId
from app.utils.db import get_db, init_db_service


init_db_service()

def upload_pdf(file_path):
    db_service = get_db()
    db = db_service.db
    fs = gridfs.GridFS(db, collection='files')
    
    with open(file_path, 'rb') as file:
        file_id = fs.put(file, filename=os.path.basename(file_path), contentType='application/pdf')
        logging.info(f'File uploaded successfully with ObjectID: {file_id}')
        return file_id


def upload_image(file_path):
    db_service = get_db()
    db = db_service.db
    fs = gridfs.GridFS(db, collection='extracted_images')
    
    with open(file_path, 'rb') as file:
        file_id = fs.put(file, filename=os.path.basename(file_path), contentType='image/jpeg')
        logging.info(f'Image uploaded successfully with ObjectID: {file_id}')
        return file_id
