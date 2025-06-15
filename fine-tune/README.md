pip install unsloth
pip install tf-keras==2.16.0 --no-dependencies


for ollama

git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release

then command sudo cp build/bin/llama-quantize . from inside llama.cpp