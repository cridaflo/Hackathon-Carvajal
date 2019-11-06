from google.cloud import storage
import os

def enviar (ruta,nombre):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Prescriptiva-911434689ac1.json"

    storage_client = storage.Client()

    buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket("prescriptivacompany-1")

    blob = bucket.blob(nombre)

    blob.upload_from_filename(ruta)

