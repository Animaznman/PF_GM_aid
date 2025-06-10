# PF_GM_aid
A tool to help Game Masters run Pathfinder 2e by processing and analyzing rulebook content.

## Setup Instructions

1. Install required Python packages:
   ```bash
   pip install PyPDF2 agentic-doc jupyter
   ```

2. Place your Pathfinder 2e PDF files in the `pdf/` directory.

3. Make .env and add LandingAI API key
   ```bash
   export VISION_AGENT_API_KEY=<your_api_key>
   ```

## Using parsePDF.ipynb

The `parsePDF.ipynb` notebook processes PDF files in two main steps:

### 1. Splitting PDFs
- The notebook first splits large PDFs into smaller 50-page chunks
- Files are saved in the `splitPDF/` directory
- Naming format: `{book_name}_{start_page}_{end_page}.pdf`
  - Example: `Pathfinder Core Rulebook_1_50.pdf`

### 2. Processing with LandingAI
- Each split PDF is processed using the LandingAI agentic-doc tool
- Results are saved in the `data/` directory
- Two files are created for each processed PDF:
  - `{book_name}_{start_page}_{end_page}.json`: Contains structured data
  - `{book_name}_{start_page}_{end_page}.md`: Contains markdown formatted text

## Usage

1. Open `parsePDF.ipynb` in Jupyter Notebook
2. Update the `pdf_file` path to point to your PDF
3. Run the cells in sequence
4. Processed files will appear in the `data/` directory

## Notes
- The script automatically creates necessary directories
- PDFs are split into 50-page chunks for optimal processing
- Each chunk is processed separately to handle large files
- Results are saved in both JSON and Markdown formats for flexibility

## Requirements
- Python 3.11+
- PyPDF2
- agentic-doc
- Jupyter Notebook


