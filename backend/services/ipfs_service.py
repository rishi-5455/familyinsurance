import os
import ipfshttpclient


def upload_file_to_ipfs(file_storage):
    """Uploads a Flask file object to IPFS and returns hash."""
    if not file_storage:
        return None

    api_url = os.getenv("IPFS_API_URL", "/dns/localhost/tcp/5001/http")
    
    try:
        with ipfshttpclient.connect(api_url) as client:
            # Save temporary bytes into IPFS add_bytes for stateless upload.
            data = file_storage.read()
            ipfs_hash = client.add_bytes(data)
            return ipfs_hash
    except Exception as e:
        # If IPFS node is not running, return a simulated hash with error info
        # This allows the app to work even without IPFS configured
        print(f"IPFS upload failed: {e}")
        return f"ipfs-unavailable-{file_storage.filename}-{len(data) if 'data' in locals() else 0}"
