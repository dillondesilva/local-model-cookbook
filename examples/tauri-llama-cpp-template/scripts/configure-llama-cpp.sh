#!/usr/bin/env bash

# This script is used to configure the llama.cpp runtime
# within the tauri-llama-cpp-template project.

# Check if runtime directory exists
if [ ! -d "../src-tauri/runtime/llama-cpp" ]; then
    echo "Runtime directory does not exist at ../src-tauri/runtime/llama-cpp"
    echo "Creating directory..."
    mkdir -p ../src-tauri/runtime/llama-cpp

    echo "Downloading llama.cpp binaries..."
    # Create a temporary directory for the download
    TMP_DIR=$(mktemp -d)

    # Download the macOS ARM64 binaries
    curl -L "https://github.com/ggml-org/llama.cpp/releases/download/b6316/llama-b6316-bin-macos-arm64.zip" -o "$TMP_DIR/llama.zip"
    
    # Check if download was successful
    if [ ! -f "$TMP_DIR/llama.zip" ]; then
        echo "Error: Failed to download llama.cpp binaries"
        rm -rf "$TMP_DIR"
        exit 1
    fi
    
    # Unzip the binaries to a temporary location
    unzip "$TMP_DIR/llama.zip" -d "$TMP_DIR/extracted"
    
    # Check if extraction was successful
    if [ ! -d "$TMP_DIR/extracted" ]; then
        echo "Error: Failed to extract llama.cpp binaries"
        rm -rf "$TMP_DIR"
        exit 1
    fi
    
    echo "Moving binaries to ../src-tauri/runtime/llama-cpp..."
    
    # Move and rename each binary with the architecture suffix
    for file in "$TMP_DIR/extracted"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            # Simple approach: add architecture suffix before any extension
            if [[ "$filename" == *.* ]]; then
                # File has extension
                name_without_ext="${filename%.*}"
                extension="${filename##*.}"
                new_filename="${name_without_ext}-aarch64-apple-darwin.${extension}"
            else
                # File has no extension
                new_filename="${filename}-aarch64-apple-darwin"
            fi
            
            echo "Copying $filename -> $new_filename"
            if cp "$file" "../src-tauri/runtime/llama-cpp/$new_filename"; then
                echo "  ✓ Successfully copied $new_filename"
            else
                echo "  ✗ Failed to copy $filename"
            fi
        fi
    done
    
    # Clean up temporary directory
    rm -rf "$TMP_DIR"
    
    echo "Binaries installed successfully!"
    echo "Files in ../src-tauri/runtime/llama-cpp:"
    ls -la ../src-tauri/runtime/llama-cpp/
else
    echo "Runtime directory already exists at ../src-tauri/runtime/llama-cpp"
    echo "Files in ../src-tauri/runtime/llama-cpp:"
    ls -la ../src-tauri/runtime/llama-cpp/
fi


