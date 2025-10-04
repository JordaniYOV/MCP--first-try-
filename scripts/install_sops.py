import os
import urllib.request


def install_sops():
    bin_dir = os.path.join(os.path.dirname(__file__), '..', 'bin')
    os.makedirs(bin_dir, exist_ok=True)
 
    url = "https://github.com/getsops/sops/releases/download/v3.11.0/sops-v3.11.0.amd64.exe"
    sops_path = os.path.join(bin_dir, "sops.exe")
    
    urllib.request.urlretrieve(url, sops_path)
    
    return sops_path

if __name__ == "__main__":
    install_sops()