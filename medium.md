# Fine-Tuning Llama 3.2 3B for Pathfinder: Creating a Specialized RPG Assistant

In this post, we'll share our journey of fine-tuning Llama 3.2 3B to create a specialized assistant for Pathfinder 2E, a popular tabletop roleplaying game. We will walk through our full pipeline—from data extraction, cleaning, fine-tuning, and deployment—with a focus on the tools and techniques we used to turn raw rulebook PDFs into a highly capable Pathfinder AI assistant.

---

### 1. Data Preparation Pipeline

The foundation of any successful fine-tuning project is high-quality data. Our primary challenge was to extract structured, usable information from the dense and complex Pathfinder 2E rulebook PDFs.

#### PDF Processing with LandingAI

The first challenge was extracting usable structured data from the thousands of pages of Pathfinder rulebooks. We leveraged LandingAI's document processing capabilities to simplify this task. LandingAI’s platform uses computer vision models to parse PDFs, which proved highly effective at interpreting the complex layouts of RPG sourcebooks.

LandingAI outputs two primary formats: Markdown and JSON. We primarily utilized the JSON files due to their structured nature, which was better suited for programmatic cleaning and processing.

Key features of LandingAI’s processing that were beneficial include:
* **Structured Text Extraction:** It successfully extracted text while preserving much of the original layout and structure.
* **Content-Type Identification:** The models could distinguish between different types of content, such as body text, tables, figures, and marginalia (side notes).
* **Metadata Preservation:** Critical metadata like page references and spatial information was retained, which helped maintain the semantic context of the source material.

This initial step allowed us to move past simple text extraction and work with a dataset that already contained much of the inherent structure of the rulebooks.

#### Data Cleaning and Structuring

Even with LandingAI’s sophisticated extraction, the raw data required significant cleaning and structuring before it was suitable for fine-tuning.

**Content Filtering:**
Our first step was to remove irrelevant content that would introduce noise into the dataset. This included:
* Marginalia, page numbers, and footers.
* Legal boilerplate such as copyright notices, licensing information, and publisher text.
* Non-game content like author credits, indexes, and tables of contents.

**Text Normalization:**
Next, we standardized the text to create a consistent format for the model.
* Unicode characters were converted into plain ASCII to avoid encoding issues.
* We standardized spacing, punctuation, and header styles across all documents.
* Redundant section titles and repeated informational headers were removed.

**Data Organization and Chunking:**
The cleaned data then needed to be organized logically.
* We used the Table of Contents—often extracted manually or with the help of an LLM due to limitations in programmatic parsing—to split the large JSON files into individual chapters. This helped preserve topical continuity.
* Oversized chapters were further subdivided into smaller chunks based on line counts. This was a pragmatic approach to keep the context size manageable for the model during the next phase.

While splitting by line count is a rudimentary method, and more advanced semantic chunking could yield better results, this approach was simple to implement and proved effective for our initial iteration.

---

### 2. Knowledge Distillation and Dataset Formatting

With the data cleaned and chunked, the next phase was to transform it into a format suitable for instruction-tuning.

#### Knowledge Distillation via Gemini 1.5 Flash

We employed a knowledge distillation strategy to convert our raw text chunks into a more focused, instructional dataset. For each chunk of text, we used Google's Gemini 1.5 Flash—a fast and highly capable model—to generate between five and ten question-and-answer (QA) pairs.

The prompts for this generation process were designed to elicit QA pairs focused on game mechanics, rules, and lore. This allowed us to transform passive, descriptive text from the rulebooks into an active, instructional format that is ideal for training an assistant model.

#### Dataset Formatting: The Alpaca Style

To format our newly generated QA pairs, we adopted the widely-used Alpaca format. This structure is specifically designed for instruction-tuning language models and is highly compatible with many popular fine-tuning pipelines.

Each entry in our dataset followed this simple JSON structure:

```json
{
  "instruction": "<The generated question about a Pathfinder rule>",
  "input": "",
  "output": "<The corresponding answer from the rulebook text>"
}
```

### 3. The Fine-Tuning Process

With a fully prepared and formatted dataset, we were ready to begin fine-tuning our chosen model.

#### Model Selection: Llama 3.2 3B

We selected Llama 3.2 3B as our base model for several key reasons:

* **Strong Instruction-Following:** The Llama 3 series is well-regarded for its ability to follow complex instructions.
* **Manageable Size:** At 3 billion parameters, it is relatively lightweight, making it feasible to fine-tune without requiring an exorbitant amount of computational resources.
* **Open-Source Support:** The model benefits from a robust open-source community and a wealth of compatible tools and libraries.

#### Training with Unsloth and LoRA

For the fine-tuning process itself, we used the **Unsloth** library, which is an optimized framework for training LLMs. Unsloth offers several significant advantages:

* **Increased Speed:** It provides approximately a 2x faster training throughput compared to standard implementations.
* **Memory Optimization:** Its memory-saving techniques allowed us to use larger batch sizes, which can improve training stability and performance.
* **QLoRA Support:** Unsloth has excellent, easy-to-use support for modern fine-tuning methods like QLoRA.

**A Deeper Look at LoRA (Low-Rank Adaptation)**

LoRA is a parameter-efficient fine-tuning (PEFT) technique that makes it possible to adapt large language models far more efficiently. Instead of updating all of the model's billions of parameters, LoRA freezes the original weights and injects small, trainable matrices (called adapters) into the model's layers.

The key benefits of this approach are:

* **Reduced Trainable Parameters:** Only a tiny fraction of the total parameters (the LoRA adapters) are updated during training.
* **Dramatically Lower Memory Usage:** This significantly reduces the GPU memory required, making it possible to fine-tune large models on more accessible, commodity hardware.
* **Faster Training:** With fewer parameters to update, the training process is much quicker.

LoRA is particularly well-suited for domain-specific tasks like ours. The base model already possesses general language capabilities; we only need to teach it the narrow, specialized knowledge of Pathfinder. LoRA allows us to do this efficiently without degrading the model's existing knowledge.

---

### 4. Environment and Deployment

To handle the computational demands of fine-tuning, we utilized powerful GPU instances from a cloud provider.

#### GPU Infrastructure with Lambda Labs

We used **Lambda Labs** to rent A100 GPU instances. Lambda provides a streamlined experience for machine learning workloads:

* **High-Performance GPUs:** Access to powerful A100 and H100 GPUs.
* **Pay-as-you-go Pricing:** A cost-effective model for project-based work.
* **Pre-configured Environments:** Instances come pre-installed with essential ML libraries like PyTorch, CUDA, and cuDNN, which simplifies the setup process.

#### Environment Setup Challenges

While the Lambda instances provided a solid foundation, we encountered some minor package dependency conflicts with Unsloth. The following steps resolved these issues and resulted in a stable training environment:

1.  **Install Unsloth:**
    ```bash
    pip install unsloth
    ```
2.  **Downgrade TensorFlow Keras:**
    Unsloth had a dependency on a specific version of TensorFlow Keras.
    ```bash
    pip install tf-keras==2.16.0 --no-dependencies
    ```
3.  **Upgrade Pillow:**
    Certain Unsloth functionalities required a more recent version of the Pillow library.
    ```bash
    pip install "Pillow>=10.0.0"
    ```
4.  **Install ipywidgets:**
    This was necessary for using some of Unsloth's interactive tools in a notebook environment.
    ```bash
    pip install ipywidgets
    ```

After performing these adjustments, our environment was ready for a smooth fine-tuning run.

#### GGUF Conversion for Local Deployment

Once fine-tuning was complete, our goal was to deploy the model in a way that was efficient and accessible. We chose the **GGUF (GPT-Generated Unified Format)** for this purpose, as it is highly optimized for inference and is the standard format for running models locally with tools like **Ollama**.

To perform the conversion, we used the `llama.cpp` library directly on the Lambda instance.

1.  **Clone and Build llama.cpp:**
    ```bash
    git clone [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
    cd llama.cpp
    cmake -B build
    cmake --build build --config Release
    ```
2.  **Make the Quantization Tool Accessible:**
    ```bash
    sudo cp build/bin/llama-quantize /usr/local/bin/
    ```

With the `llama-quantize` tool available, we could convert our fine-tuned model into various quantized GGUF versions. Quantization further reduces the model's size and computational requirements, making it possible to run on consumer-grade hardware with minimal performance loss.

### Step 5: Download Fine-tuned Model and Set up Ollama Locally

First create a Modelfile in the same folder as the GGUF and make sure it has the same format that the model was fine-tuned on, for us this was Alpaca style.

```plaintext
FROM ./unsloth.Q4_K_M.gguf

TEMPLATE """<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
PARAMETER temperature 0.7
PARAMETER top_p 0.9

SYSTEM """You are a knowledgeable expert on the world of Golarion from Pathfinder RPG."""
```

This step outlines how to download your fine-tuned Ollama model and its corresponding Modelfile from a remote instance, and then set up this model locally with Ollama.

#### 5.1 Download Ollama Model and Modelfile from the Instance

First, you need to securely copy the fine-tuned model and Modelfile from your remote instance to your local machine. Replace `<instance_ip_address>` with the actual IP address of your remote instance.

```bash
# Download the 'ollama_model' directory containing your fine-tuned model
scp -r ubuntu@<instance_ip_address>:/home/ubuntu/PF_GM_aid/fine-tune/ollama_model ./

# Download the 'Modelfile' used to create your fine-tuned model
scp -r ubuntu@<instance_ip_address>:/home/ubuntu/PF_GM_aid/fine-tune/Modelfile ./
```
Once the files are downloaded, you'll move the Modelfile into the ollama_model directory and then use Ollama to create and run your fine-tuned model.

```bash
# Navigate to the directory where the 'ollama_model' and 'Modelfile' were downloaded
# (Assuming they were downloaded to your current working directory)
# If downloaded elsewhere, replace 'cd' with the appropriate path.
cd ollama_model

# Move the Modelfile into the ollama_model directory.
# This is crucial because the 'ollama create' command will look for the Modelfile within the context directory.
mv ../Modelfile .

# Create the Ollama model using the Modelfile.
# 'pathfinder-gm' is the name you are assigning to your local Ollama model.
# The '-f Modelfile' flag specifies the Modelfile to use for creation.
ollama create pathfinder-gm -f Modelfile

# Run your newly created Ollama model.
# This command will start an interactive session with your fine-tuned 'pathfinder-gm' model.
ollama run pathfinder-gm
```

---

### 5. Results and Deployment

After the fine-tuning and conversion processes were complete, we saved the model in two key formats:

1.  **LoRA Adapter:** We saved the trained LoRA adapter separately. This allows for future incremental fine-tuning. As we gather more data or as new rulebooks are released, we can easily continue training from where we left off without starting from scratch.
2.  **Merged, Quantized Model:** We also merged the LoRA adapter with the base model's weights to create a standalone model. This merged model was then converted into the GGUF format for easy deployment.

By using **Ollama**, a platform for serving and running local LLMs, our final Pathfinder Assistant can be run entirely on a local machine. This provides fast, private, and offline-capable responses without the need for external API calls.

### Conclusion

This project demonstrates how a combination of modern open-source AI tools can be leveraged to create a highly specialized language model with relatively modest resources. The pipeline of:

* **LandingAI** for intelligent document processing,
* A **custom data cleaning pipeline** for structuring the data,
* **Llama 3.2 3B + Unsloth + LoRA** for efficient fine-tuning,
* **Lambda Labs** for scalable GPU access,
* And **Ollama** for private, local inference

...allowed us to successfully build a functional Pathfinder RPG assistant capable of answering detailed questions about the game's rules, lore, and mechanics. This approach can be replicated for numerous other niche domains where expert-level knowledge remains locked within complex documents.