#!/usr/bin/env python3
"""
Script to install llama.cpp runtime based on runtimes.yaml configuration.
This script loads the runtime configuration and provides installation options.
"""
import sys
import os
import json
import logging
import zipfile
import urllib.request
import shutil
from pathlib import Path

def load_runtimes_config():
    """Load the runtimes.json configuration file."""
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / "runtimes.json"
    
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.critical(f"Fatal error: runtimes.json not found at {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.critical(f"Fatal error: Error parsing runtimes.json: {e}")
        sys.exit(1)

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that a directory exists at the given path, creating it if necessary.
    
    Args:
        directory_path: String path to the directory that should exist
    """
    full_path = Path(os.getcwd()) / directory_path
    try:
        full_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Ensured directory exists at: {full_path}")
    except Exception as e:
        logging.error(f"Failed to create directory at {full_path}: {e}")
        sys.exit(1)

def download_binary(lts_version: str, platform: str, downloads_dir: str) -> None:
    """
    Download a binary from the given URL and save it to the given path.
    """
    full_path = Path(os.getcwd()) / downloads_dir / f"llama-b{lts_version}-bin-{platform}.zip"
    url = f"https://github.com/ggerganov/llama.cpp/releases/download/{lts_version}/llama-b6332-bin-{platform}.zip"
    print(f"Downloading {url}...")

    logging.info(f"Downloading {url}...")
    urllib.request.urlretrieve(url, str(full_path))
    print(f"Downloaded {url} to {full_path}")
    unzip_binary(full_path, platform)

def unzip_binary(zip_path: Path, platform: str) -> None:
    """
    Unzip the binary from the given path
    """
    print(f"Unzipping {zip_path}...")
    extract_dir = zip_path.parent
    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in z.infolist():
            original_name = member.filename
            # Skip directories
            if member.is_dir():
                continue

            new_name = f"{original_name}-{platform}"
            new_path = os.path.join(extract_dir, new_name)

            # Ensure parent directory exists
            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            # Extract and rename
            with z.open(member) as source, open(new_path, "wb") as target:
                target.write(source.read())

def main():
    """Main function to run the script."""
    logging.info("Loading runtime configuration...")
    config = load_runtimes_config()
    lts_release = config['runtimes']['llama-cpp']['latest-alchemist-supported-release']
    latest_prebuilt_binary_releases = config['runtimes']['llama-cpp']['versions'][lts_release]['installations']
    downloads_dir = "runtime/llama-cpp"
    ensure_directory_exists(downloads_dir)
    for platform, sha256 in latest_prebuilt_binary_releases.items():
        logging.info(f"Downloading {platform} binary...")
        print(platform, sha256)
        download_binary(lts_release, platform, downloads_dir)
    print("\n✅ Runtime configuration loaded successfully!")
    print("This script is ready to handle llama.cpp runtime installation.")

main()
