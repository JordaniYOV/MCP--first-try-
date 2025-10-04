import os
import subprocess
import yaml
import json
from pathlib import Path

def get_sops_path():
    project_root = Path(__file__).parent.parent
    sops_path = project_root / "bin" / "sops.exe"
    
    if not sops_path.exists():
        raise FileNotFoundError(f"SOPS не найден. Запустите scripts/install_sops.py")
    
    return str(sops_path)

def decrypt_file(encrypted_file, age_key_path):
    """Дешифрует SOPS файл"""
    sops_path = get_sops_path()
    env = os.environ.copy()
    env["SOPS_AGE_KEY_FILE"] = age_key_path

    cmd = [sops_path, "--decrypt", encrypted_file]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        with open(encrypted_file, 'w') as f:
                f.write(result.stdout)
            
    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка дешифровки: {e.stderr}")

def encrypt_file(input_file, output_file, age_key):
    """Шифрует файл с помощью SOPS"""
    sops_path = get_sops_path()
    
    cmd = [sops_path, "--age", age_key, "--encrypt", input_file, '>', 'wd.enc.json']

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        with open(output_file, 'w') as f:
                f.write(result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка шифровки: {e.stderr}")

def get_value(encrypted_file, age_key_file, key_path):
        """Получает конкретное значение из зашифрованного файла"""
        sops_path = get_sops_path()
        env = os.environ.copy()
        env["SOPS_AGE_KEY_FILE"] = age_key_file

        cmd = [sops_path, '--decrypt', '--extract', key_path, encrypted_file]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(result.stdout)
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to extract value: {e.stderr}")

# def edit_encrypted_file(encrypted_file, age_key_file):
    # """Редактирует зашифрованный файл"""
    # sops_path = get_sops_path()
    
    # env = os.environ.copy()
    # if age_key_file:
    #     env["SOPS_AGE_KEY_FILE"] = age_key_file
    
    # subprocess.run([sops_path, str(encrypted_file)], env=env, check=True)


if __name__ == "__main__": 
    # encrypt_file('tokens.json', 'tokensenc.json', 'age18g37p7tfqlrsp3szpkrkmv4lqzwp2cwsz8kwql8n978eknuypqzqrpukys')
    # decrypt_file('tokensenc.json', 'key.txt')
    get_value('tokensenc.json', 'key.txt', '["expires_in"]')
