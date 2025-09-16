---
sidebar_position: 1
---

# Build a Local LM Tauri App

## Quick Start

1. Clone the example repository:
   ```bash
   git clone https://github.com/dillondesilva/local-model-cookbook.git
   cd local-model-cookbook/examples/tauri-llama-cpp-template
   ```

2. Run the script to install the [llama.cpp](https://github.com/ggml-org/llama.cpp) runtime and unzip binaries into relevant location:
   ```bash
   python install_llama_cpp_runtime.py
   ```

3. Follow the setup instructions in the repository's README to build and run your desktop application.

## Key Concepts

Tauri is a framework for building lightweight desktop applications using web technologies (JS/TS) and Rust. The architecture leverages `llama.cpp` as a sidecar process managed by Tauri, allowing the frontend to communicate with the local model through HTTP requests while keeping all processing on the user's device. This approach provides complete privacy, offline functionality and modern web development capabilities while maintaining native desktop performance and security.

For the original reference application (Mac-Only), check out the [tauri-local-lm repository](https://github.com/dillondesilva/tauri-local-lm).
