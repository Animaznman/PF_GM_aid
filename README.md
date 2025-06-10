# PF_GM_aid
A tool to help Game Masters run Pathfinder 2e by processing and analyzing rulebook content.

## Project Structure
```
PF_GM_aid/
├── pdf/                    # Directory for original PDF files
│   └── .gitkeep
├── splitPDF/              # Directory for split PDF files
│   └── .gitkeep
├── data/                  # Directory for processed data
│   └── .gitkeep
├── parsePDF.ipynb         # Jupyter notebook for PDF processing
└── README.md             # This file
```

## Setup Instructions

1. Create the required directory structure:
   ```bash
   mkdir -p pdf splitPDF data
   touch pdf/.gitkeep splitPDF/.gitkeep data/.gitkeep
   ```

2. Install required Python packages:
   ```bash
   pip install PyPDF2 agentic-doc jupyter
   ```

3. Place your Pathfinder 2e PDF files in the `pdf/` directory.

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


