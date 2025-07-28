# 📄 PDF Document Structure Extraction – Challenge 1A

> **An intelligent PDF processing system that extracts hierarchical document structures and generates structured JSON outputs for document analysis and indexing.**

This solution processes PDF documents to extract titles, headings, and hierarchical structure using advanced text analysis and formatting detection, optimized for the Adobe India Hackathon 2025.

---

## 🎯 Challenge Overview

**Challenge 1A** focuses on developing a high-performance PDF processing system that can:
- Extract document titles and hierarchical headings (H1, H2, H3)
- Process PDFs automatically from input directories
- Generate structured JSON outputs with document metadata
- Meet strict performance and resource constraints
- Run in containerized environments without network access

---

## 🏗️ Project Structure

```
challange_1a/
├── app/
│   ├── input/                      # Input PDF files for processing
│   │   ├── file01.pdf             # Sample PDF documents
│   │   ├── file02.pdf
│   │   ├── file03.pdf
│   │   ├── file04.pdf
│   │   └── file05.pdf
│   └── output/                     # Generated JSON output files
│       ├── file01.json            # Extracted structure data
│       ├── file02.json
│       ├── file03.json
│       ├── file04.json
│       └── file05.json
├── pdf_process.py                  # Main processing engine
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
└── README.md                       # This documentation
```

---

## 🔧 Technical Implementation

### Core Processing Engine

**`pdf_process.py`** - Advanced PDF analysis system featuring:

1. **Document Title Detection**
   - Bold text analysis for primary titles
   - Font size-based title identification
   - Fallback mechanisms for complex layouts
   - Text cleaning and normalization

2. **Hierarchical Heading Extraction**
   - Multi-level heading detection (H1, H2, H3)
   - Font size and formatting analysis
   - Table of Contents context awareness
   - Numbered section recognition

3. **Advanced Text Analysis**
   - spaCy NLP integration for text understanding
   - Formatting characteristic analysis (bold, italic, font size)
   - Context-aware filtering (TOC exclusion)
   - Structural consistency validation

### Key Features

- ✅ **Intelligent Title Detection**: Multi-strategy approach for accurate title extraction
- ✅ **Hierarchical Structure**: Automatic H1/H2/H3 classification
- ✅ **NLP Integration**: spaCy-powered text analysis for better accuracy
- ✅ **Performance Optimized**: Processes documents within 10-second constraint
- ✅ **Memory Efficient**: Operates within 16GB RAM limits
- ✅ **Container Ready**: Fully containerized with Docker

---

## 📋 Official Challenge Requirements

### Performance Constraints

| Requirement | Specification |
|-------------|---------------|
| **Execution Time** | ≤ 10 seconds for 50-page PDF |
| **Memory Usage** | ≤ 16GB RAM |
| **CPU Architecture** | AMD64 (8 CPUs) |
| **Model Size** | ≤ 200MB (if using ML models) |
| **Network Access** | None (offline processing only) |

### Technical Requirements

- 🔒 **Input Directory**: Read-only access to `/app/input`
- 📄 **Output Format**: Generate `filename.json` for each `filename.pdf`
- 🌐 **Open Source**: All libraries and tools must be open source
- 🐳 **Containerized**: Must run in Docker with network isolation
- ⚡ **Automatic Processing**: Batch process all PDFs in input directory

---

## 📥 Input Processing

The system automatically processes all PDF files from the `/app/input` directory:

```
app/input/
├── file01.pdf    # Application form document
├── file02.pdf    # RFP request document  
├── file03.pdf    # Multi-section technical document
├── file04.pdf    # Simple overview document
└── file05.pdf    # RSVP invitation document
```

---

## 📤 Output Format

Generated JSON files contain structured document analysis:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Section Heading",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Subsection Heading",
      "page": 2
    },
    {
      "level": "H3",
      "text": "Sub-subsection Heading", 
      "page": 3
    }
  ]
}
```

### Output Structure Details

- **`title`**: Extracted document title (string or null)
- **`outline`**: Array of hierarchical headings
  - **`level`**: Heading level ("H1", "H2", "H3")
  - **`text`**: Heading text content
  - **`page`**: Page number where heading appears

---

## 🚀 How to Run

### Method 1: Docker Container (Recommended)

```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-extractor:3 .

# Run with proper volume mounting
docker run --rm \
  -v "$(pwd)/app:/app/app" \
  --network none \
  pdf-extractor:3

# For Windows PowerShell:
docker run --rm `
  -v "${PWD}/app:/app/app" `
  --network none `
  pdf-extractor:3
```

### Method 2: Python Direct Execution

```bash
# Navigate to project directory
cd challange_1a

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (one-time setup)
python -m spacy download en_core_web_sm

# Run the processor
python pdf_process.py
```

### Method 3: Official Challenge Format

```bash
# Build with official naming
docker build --platform linux/amd64 -t adobe-challenge-1a .

# Run with official volume structure
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-challenge-1a
```

---

## 📊 Processing Results

Successful execution produces:

```
2025-07-28 20:22:31,591 - INFO - Processing file01.pdf
2025-07-28 20:22:31,677 - INFO - Successfully processed file01.pdf
2025-07-28 20:22:32,022 - INFO - Processing file02.pdf
2025-07-28 20:22:32,437 - INFO - Successfully processed file02.pdf
2025-07-28 20:22:32,437 - INFO - Processing file03.pdf
2025-07-28 20:22:32,437 - INFO - Successfully processed file03.pdf
2025-07-28 20:22:32,438 - INFO - Processing file04.pdf
2025-07-28 20:22:32,450 - INFO - Successfully processed file04.pdf
2025-07-28 20:22:32,450 - INFO - Processing file05.pdf
2025-07-28 20:22:32,460 - INFO - Successfully processed file05.pdf
```

Output files generated:
- ✅ `file01.json` - Application form structure
- ✅ `file02.json` - RFP document outline  
- ✅ `file03.json` - Technical document hierarchy
- ✅ `file04.json` - Overview document structure
- ✅ `file05.json` - RSVP invitation outline

---

## 🔍 Algorithm Details

### Title Extraction Strategy

1. **Bold Text Analysis**: Identify bold formatted text blocks
2. **Font Size Ranking**: Prioritize larger font sizes
3. **Position Analysis**: Consider document positioning
4. **Text Cleaning**: Remove artifacts and normalize content
5. **Fallback Methods**: Multiple strategies for complex layouts

### Heading Classification Logic

```python
# Heading level determination
if font_size >= 18 and is_bold and len(text.split()) < 10:
    level = "H1"  # Primary headings
elif 12 <= font_size < 18:
    level = "H2"  # Secondary headings  
elif 10.5 <= font_size < 12 and conditions_met:
    level = "H3"  # Tertiary headings
```

### Advanced Features

- **TOC Context Awareness**: Excludes table of contents entries
- **Numbered Section Detection**: Handles "1.1", "Phase I", etc.
- **Multi-span Analysis**: Processes complex formatting
- **Error Handling**: Robust processing for malformed PDFs

---

## 🛠️ Dependencies

```txt
PyMuPDF==1.24.1     # PDF processing and text extraction
spacy==3.7.2        # Natural language processing
en_core_web_sm      # English language model for spaCy
```

### Dependency Details

- **PyMuPDF (fitz)**: High-performance PDF text extraction
- **spaCy**: Advanced NLP for text analysis and classification
- **en_core_web_sm**: Compact English model for text understanding

---

## 🐳 Docker Configuration

**Dockerfile Features:**
- **Base Image**: `python:3.9-alpine` for minimal footprint
- **Platform**: `linux/amd64` for challenge compatibility
- **Dependencies**: Optimized installation with build cleanup
- **spaCy Model**: Automatic download and setup
- **Entry Point**: Direct execution of `pdf_process.py`

```dockerfile
# Optimized Alpine-based container
FROM --platform=linux/amd64 python:3.9-alpine

# Install system dependencies
RUN apk add --no-cache libstdc++ && \
    apk add --no-cache --virtual .build-deps build-base python3-dev && \
    pip install --no-cache-dir PyMuPDF spacy && \
    python -m spacy download en_core_web_sm && \
    apk del .build-deps

# Setup application
WORKDIR /app
COPY pdf_process.py .
CMD ["python", "pdf_process.py"]
```

---

## ✅ Validation Checklist

### Functional Requirements
- [x] **PDF Processing**: All PDFs in input directory processed
- [x] **JSON Generation**: Corresponding JSON files created
- [x] **Structure Extraction**: Titles and headings properly identified
- [x] **Hierarchical Classification**: Correct H1/H2/H3 assignment
- [x] **Error Handling**: Graceful handling of malformed PDFs

### Performance Requirements
- [x] **Execution Time**: < 10 seconds for test documents
- [x] **Memory Usage**: Efficient memory management
- [x] **CPU Optimization**: Utilizes available processing power
- [x] **Network Isolation**: No external dependencies during runtime
- [x] **AMD64 Compatibility**: Runs on target architecture

### Quality Assurance
- [x] **Output Format**: Valid JSON structure
- [x] **Content Accuracy**: Meaningful title and heading extraction
- [x] **Robustness**: Handles various PDF layouts and complexities
- [x] **Logging**: Comprehensive processing information
- [x] **Container Isolation**: Secure containerized execution

---

## 📚 Additional Notes

### Performance Optimizations
- Efficient PDF parsing with PyMuPDF
- Minimal memory footprint with Alpine Linux
- Optimized spaCy model loading
- Streamlined text processing pipelines

### Extensibility
- Modular design for easy enhancement
- Configurable heading detection parameters
- Support for additional output formats
- Scalable to larger document collections

### Security Features
- Network isolation during execution
- Read-only input directory access
- No external API dependencies
- Containerized execution environment

---

## 📄 License

This project is developed for the Adobe India Hackathon 2025. All code and implementations are provided for educational and competition purposes.

---

**🎯 Ready to extract structured intelligence from your PDF documents!** 