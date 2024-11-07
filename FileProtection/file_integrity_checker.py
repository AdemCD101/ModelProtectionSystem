# file_integrity_checker.py
import hashlib
import os
import logging

# Configure logging
logging.basicConfig(
    filename='file_integrity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def calculate_hash(file_path):
    """
    计算文件的哈希值，用于检查文件的完整性。
    :param file_path: 文件路径
    :return: 文件的SHA-256哈希值
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return None

def verify_file_integrity(file_path, expected_hash):
    """
    验证文件的完整性，检查哈希值是否与预期值一致。
    :param file_path: 文件路径
    :param expected_hash: 预期的哈希值
    :return: 是否通过完整性检查
    """
    current_hash = calculate_hash(file_path)
    if current_hash == expected_hash:
        logging.info(f"File integrity verified for {file_path}.")
        return True
    else:
        logging.warning(f"File integrity check failed for {file_path}. Expected: {expected_hash}, Got: {current_hash}")
        return False

if __name__ == "__main__":
    TEST_FILE = r"D:\\SteamLibrary\\steamapps\\common\\VTube Studio\\VTube Studio_Data\\StreamingAssets\\Live2DModels\\ShanLan-test\\ShanLan-Basic.moc3"
    EXPECTED_HASH = "your_expected_hash_here"
    verify_file_integrity(TEST_FILE, EXPECTED_HASH)