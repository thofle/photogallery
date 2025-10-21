"""
Photo Gallery Frontend for Azure Storage Account
"""
import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Azure Storage configuration
STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'photobooth')


def get_blob_service_client():
    """Get Azure Blob Service Client"""
    if CONNECTION_STRING:
        return BlobServiceClient.from_connection_string(CONNECTION_STRING)
    elif STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY:
        account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
        from azure.storage.blob import BlobServiceClient
        return BlobServiceClient(account_url=account_url, credential=STORAGE_ACCOUNT_KEY)
    else:
        raise ValueError("Azure Storage credentials not configured")


def get_blob_url_with_sas(blob_name, container_name=CONTAINER_NAME):
    """Generate a SAS URL for a blob"""
    if not STORAGE_ACCOUNT_NAME or not STORAGE_ACCOUNT_KEY:
        return None
    
    sas_token = generate_blob_sas(
        account_name=STORAGE_ACCOUNT_NAME,
        container_name=container_name,
        blob_name=blob_name,
        account_key=STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    
    return f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"


def list_blobs_in_folder(gallery_id):
    """List all blobs in the photobooth/<id> folder"""
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        prefix = f"{gallery_id}/"
        blobs = []
        
        for blob in container_client.list_blobs(name_starts_with=prefix):
            # Get relative path within the gallery folder
            relative_name = blob.name[len(prefix):]
            
            # Skip the zip file and any subdirectories for the gallery display
            if relative_name and not '/' in relative_name:
                # Determine if it's an image or the zip file
                is_image = any(relative_name.lower().endswith(ext) 
                             for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'])
                is_zip = relative_name.lower().endswith('.zip')
                
                if is_image or is_zip:
                    blob_info = {
                        'name': relative_name,
                        'full_name': blob.name,
                        'url': get_blob_url_with_sas(blob.name),
                        'size': blob.size,
                        'is_image': is_image,
                        'is_zip': is_zip
                    }
                    blobs.append(blob_info)
        
        # Separate images and zip file
        images = [b for b in blobs if b['is_image']]
        zip_file = next((b for b in blobs if b['is_zip']), None)
        
        return images, zip_file
    
    except Exception as e:
        print(f"Error listing blobs: {e}")
        return [], None


@app.route('/')
def index():
    """Homepage with input for gallery ID"""
    return render_template('index.html')


@app.route('/gallery/<gallery_id>')
def gallery(gallery_id):
    """Display the photo gallery for the given ID"""
    if not gallery_id:
        return redirect(url_for('index'))
    
    images, zip_file = list_blobs_in_folder(gallery_id)
    
    return render_template('gallery.html', 
                         gallery_id=gallery_id, 
                         images=images, 
                         zip_file=zip_file)


@app.route('/view')
def view_gallery():
    """Redirect to gallery based on form input"""
    gallery_id = request.args.get('id', '')
    if gallery_id:
        return redirect(url_for('gallery', gallery_id=gallery_id))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
