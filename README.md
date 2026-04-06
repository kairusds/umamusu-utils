# Umamusu-Utils

Utils for scrapping honse game files.

## Requirements

**Python 3.12+**

You must put your copy of the `meta` file in the `storage` folder.

You can grab the `meta` file from these folders:

**Android (if you have external documents provider patched to the game or a rooted device)**: `/data/data/jp.co.cygames.umamusume/files`

**For Windows, refer to** [the Hachimi Edge FAQ](https://hachimi.noccu.art/docs/hachimi/faqs#how-do-i-find-the-game-install-folder) to find the game's base folder and find the `meta` file under the subfolders: `UmamusumePrettyDerby_Jpn_Data\Persistent` or `umamusume_Data\Persistent`.

### Activating venv for using the scripts

Run these commands:

**Linux**

```
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```
python -m venv .venv
.venv\Scripts\activate.bat
```
**If `activate.bat` didn't work**: `.venv\Scripts\Activate.ps1`

(Note: If you get an error saying something like "scripts is disabled on this system," you need to **run your terminal app as an Administrator** and run this command once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.)

### Install dependencies

Afterwards, run `pip install -r requirements.txt` to install all dependencies of the scripts.

## Utils

All utils reside inside the `scripts` folder. Run them with `python scripts/SCRIPTNAME.py`.

### `data_download.py`

Downloads **ALL** game assets according to your `meta` file.
If the game is updated, all you have to do is update the `meta` file and re-run this script.
This only downloads new files, you can set `SKIP_EXISTING` to `False` inside the script to force a full re-download.

Set `HPATHS` inside of the script to `True` if you want the downloaded folder structure to be the same as the game's `dat` folder structure.

**IMPORTANT** If doing a full download, this will suck your machine's network dry.
Set `ASYNC_DOWNLOAD` to `False` to download in a less aggressive way.

Uses the decrypted meta file if `decrypt_meta.py` was used before this script.

The output files are located at `storage/data (storage/dat if HPATHS is set to True)`.

### `items_extract.py`

Extracts stuff related to items. Output file can be found at `storage/items.txt`.

### `story_extract.py`

Extracts the strings related to the in-game stories.
This only extracts new files, you can set `SKIP_EXISTING` to `False` inside the script to force a full extraction.

Uses the decrypted assets if `decrypt_assets.py` was used before this script.

Set `HPATHS` inside of the script to `True` if you also set `HPATHS` to `True` in `data_download.py`.

The output files are located at `storage/story`.

### `decrypt_meta.py`

Creates a one-to-one copy of the `meta` file with no encryption. Output file can be found at `storage/meta_decrypted`.

### `decrypt_assets.py`

Creates a one-to-one copy of the asset files from the `storage/data` folder with no encryption.

Set `HPATHS` inside of the script to `True` if you also set `HPATHS` to `True` in `data_download.py`.

Can be customized which folders are included or excluded and whether to skip existing files with these lines of code inside the script:

```
# Skip existing decrypted assets
SKIP_EXISTING = True

# If this is NOT empty, ONLY assets within these folders will be decrypted.
# If this IS empty, ALL assets will be processed (with exclusions).
# Example:
# INCLUDED_FOLDERS = set()
# INCLUDED_FOLDERS = {"sound/v/", "story/data/"}
INCLUDED_FOLDERS = {"story/data/"}

# Any asset from these folders will be explicitly SKIPPED.
# This is useful for ignoring entire categories of files.
# Example:
# EXCLUDED_FOLDERS = {"font/"}
# EXCLUDED_FOLDERS = {"font/", "movie/"}
EXCLUDED_FOLDERS = set()
```

The output files are located at `storage/data_decrypted`.

### `dump_meta.py`

Dumps the contents of the meta file into a JSON file.

**WARNING** The output file might be over 50MB, do not open the dump file with a normal text editor on a phone or PC.
It's recommended to view the file with something like `neovim` or `vim` instead.

Output file can be found at `storage/meta_dump.json`.

### `extract_textures.py`

Extracts `Texture2D` and `Sprite` assets from Unity bundles into PNG files.

Set `HPATHS` inside of the script to `True` if you also set `HPATHS` to `True` in `data_download.py`.

```
# Skip existing extracted assets
SKIP_EXISTING = True

# If this is NOT empty, ONLY assets within these folders will be processed.
# If this IS empty, ALL assets will be processed (with exclusions).
# Example:
# INCLUDED_FOLDERS = set()
# Example: INCLUDED_FOLDERS = {"atlas/"}
# Example: INCLUDED_FOLDERS = {"atlas/rank/", "atlas/statusrank", "uianimation/"}
INCLUDED_FOLDERS = {"atlas/rank/", "atlas/statusrank", "uianimation/"}

# Any asset from these folders will be explicitly SKIPPED.
EXCLUDED_FOLDERS = set()
```

The output files are located at `storage/extracted_textures`.
