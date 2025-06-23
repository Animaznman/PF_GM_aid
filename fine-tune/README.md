# Setup Instructions

## SSH Key Setup and Repository Cloning

### 1. Generate SSH Key
```bash
ssh-keygen
```

### 2. Get Public Key
```bash
cat ~/.ssh/id_rsa.pub
```

### 3. Add Public Key to GitHub
Add the public key output to your GitHub account under Settings > SSH and GPG keys

### 4. Clone Repository
```bash
git clone git@github.com:Animaznman/PF_GM_aid.git
```

### 5. Navigate to Fine-tune Folder
```bash
cd PF_GM_aid/fine-tune
```

## Python Dependencies Installation

```bash
pip install unsloth
pip install tf-keras==2.16.0 --no-dependencies
pip install "Pillow>=10.0.0"
pip install ipywidgets
```

## Model Export to Ollama

### 1. Clone and Build llama.cpp
```bash
sudo apt update
sudo apt install libcurl4-openssl-dev

git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

### 2. Copy Quantization Tool
```bash
sudo cp build/bin/llama-quantize .
```

## Download Model Files

### Download Ollama Model and Modelfile
```bash
scp -r ubuntu@167.234.210.45:/home/ubuntu/PF_GM_aid/fine-tune/ollama_model ./
scp -r ubuntu@167.234.210.45:/home/ubuntu/PF_GM_aid/fine-tune/Modelfile ./
```

## Set up Ollama Locally

Navigate where the files were downloaded to, and move the Modelfile into the ollama_model folder

```bash
cd ollama_model
ollama create pathfinder-gm -f Modelfile
ollama run pathfinder-gm                
```
