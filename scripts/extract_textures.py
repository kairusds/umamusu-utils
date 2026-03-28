import os
import UnityPy
from pathlib import Path
from PIL import Image

from utils import get_meta_conn, get_storage_folder, get_logger, _derive_asset_key

logger = get_logger(__name__)
SKIP_EXISTING = True
HPATHS = False 

if HPATHS:
    DATA_ROOT = get_storage_folder("dat")
else:
    DATA_ROOT = get_storage_folder("data")

EXTRACT_ROOT = get_storage_folder("extracted_textures")
BLOB_TABLE = "a"

# If this is NOT empty, ONLY assets within these folders will be processed.
# If this IS empty, ALL assets will be processed (with exclusions).
# Example:
# INCLUDED_FOLDERS = set()
# Example: INCLUDED_FOLDERS = {"atlas/"}
# Example: INCLUDED_FOLDERS = {"atlas/rank/", "atlas/statusrank", "uianimation/"}
INCLUDED_FOLDERS = {"atlas/rank/", "atlas/statusrank", "uianimation/"}

# Any asset from these folders will be explicitly SKIPPED.
EXCLUDED_FOLDERS = set()

def extract_textures():
    logger.info("Starting texture extraction process...")
    meta_conn = None
    
    try:
        meta_conn = get_meta_conn()
        query = f'SELECT "n", "h", "e" FROM "{BLOB_TABLE}"'
        all_assets = list(meta_conn.execute(query))
        total_assets = len(all_assets)
        logger.info(f"Found {total_assets} assets from meta.")
        
        for row in all_assets:
            db_asset_name = row["n"]
            asset_key = row["e"]

            if any(db_asset_name.startswith(f) for f in EXCLUDED_FOLDERS):
                logger.info(f"Skipping file in excluded folder: {db_asset_name}...")
                continue
            if INCLUDED_FOLDERS and not any(db_asset_name.startswith(f) for f in INCLUDED_FOLDERS):
                continue

            source_path = Path(DATA_ROOT, db_asset_name)
            if not source_path.exists():
                continue

            try:
                with open(source_path, "rb") as f:
                    data = bytearray(f.read())

                if asset_key != 0:
                    decryption_key = _derive_asset_key(asset_key)
                    if decryption_key and len(data) > 256:
                        key_len = len(decryption_key)
                        for j in range(256, len(data)):
                            data[j] ^= decryption_key[j % key_len]

                env = UnityPy.load(bytes(data))
                
                for obj in env.objects:
                    if obj.type.name in ["Texture2D", "Sprite"]:
                        data_obj = obj.read()

                        asset_name = getattr(data_obj, "m_Name", Path(db_asset_name).stem)

                        target_dir = Path(EXTRACT_ROOT, db_asset_name).parent
                        target_dir.mkdir(parents=True, exist_ok=True)
                        dest_path = Path(target_dir, f"{asset_name}.png")

                        if SKIP_EXISTING and dest_path.exists():
                            continue

                        try:
                            img = data_obj.image
                            if img:
                                img.save(dest_path)
                                logger.info(f"Extracted: {db_asset_name} -> {asset_name}.png")
                        except Exception as img_err:
                            logger.error(f"Could not convert texture {asset_name} in {db_asset_name}: {img_err}")

            except Exception as e:
                logger.error(f"Failed to process {db_asset_name}: {e}")

    finally:
        if meta_conn:
            meta_conn.close()
    
    logger.info("Extraction complete.")

if __name__ == "__main__":
    extract_textures()
