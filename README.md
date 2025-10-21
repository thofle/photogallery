# Photo Gallery - Azure Storage Frontend

A simple and elegant web-based photo gallery frontend for Azure Storage Account. This application allows users to view photos stored in Azure Blob Storage and download them as a ZIP file.

## Features

- 🖼️ **Gallery View**: Browse photos in a beautiful grid layout
- 📦 **ZIP Download**: Download all photos in a gallery as a single ZIP file
- 🔐 **Secure Access**: Uses Azure SAS tokens for secure blob access
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- ⚡ **Fast Loading**: Lazy loading for images to optimize performance

## Prerequisites

- Python 3.8 or higher
- Azure Storage Account with a container named `photobooth`
- Photos organized in folders: `photobooth/<id>/`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thofle/photogallery.git
cd photogallery
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Azure Storage credentials:

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Azure Storage credentials:
   ```
   AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
   AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
   # OR use connection string instead:
   # AZURE_STORAGE_CONNECTION_STRING=your_connection_string
   CONTAINER_NAME=photobooth
   ```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a gallery ID to view photos from `https://<storage-account>/photobooth/<id>/`

## Azure Storage Structure

The application expects the following structure in your Azure Storage container:

```
photobooth/
├── gallery-id-1/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   ├── photo3.png
│   └── gallery-id-1.zip
├── gallery-id-2/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── gallery-id-2.zip
```

- Each gallery has its own folder under the `photobooth` container
- Photos should be directly in the gallery folder (not in subfolders)
- A ZIP file with the same name as the gallery ID should be present for download functionality
- Supported image formats: JPG, JPEG, PNG, GIF, WEBP, BMP

## Configuration Options

You can configure the application using environment variables in the `.env` file:

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_STORAGE_ACCOUNT_NAME` | Azure Storage account name | Yes* |
| `AZURE_STORAGE_ACCOUNT_KEY` | Azure Storage account key | Yes* |
| `AZURE_STORAGE_CONNECTION_STRING` | Alternative to account name/key | Yes* |
| `CONTAINER_NAME` | Name of the blob container | No (default: `photobooth`) |

*Either provide `AZURE_STORAGE_CONNECTION_STRING` or both `AZURE_STORAGE_ACCOUNT_NAME` and `AZURE_STORAGE_ACCOUNT_KEY`

## Development

To run the application in development mode with debug enabled:

```bash
python app.py
```

The application will be available at `http://0.0.0.0:5000` with auto-reload enabled.

## Security Notes

- SAS tokens are generated with 1-hour expiration for secure blob access
- The `.env` file containing credentials is excluded from version control
- Never commit your Azure credentials to the repository

## License

This project is open source and available under the MIT License.