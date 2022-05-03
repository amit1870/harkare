# harkare
Path to SiyaRam

## Install MinIO and run the binary if downloaded
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password ./minio server /mnt/data --console-address ":9001"

## Install dependencies in vitual env to avoid breaking systems
pip install -r requirements.txt
