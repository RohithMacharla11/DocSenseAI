# 🧠 Persona-Driven Document Intelligence – Challenge 1B

> **An intelligent document analysis system that extracts relevant content from PDF collections based on user personas and specific job requirements.**

This system processes multiple PDF collections and delivers context-aware content extraction using persona-driven analysis, making it ideal for domain-specific document intelligence tasks.

---

## 🎯 Challenge Overview

**Challenge 1B** focuses on developing a persona-aware document processing system that can:
- Analyze PDF collections from different domains (Travel, HR, Food)
- Extract relevant content based on user personas and their specific tasks
- Generate structured JSON outputs with metadata and analysis insights
- Process documents efficiently using containerized deployment

---

## 🏗️ Project Structure

```
challange_1b/
├── Collection 1/                    # Travel Planning Documents
│   ├── PDFs/                       # 7 travel-related PDF files
│   ├── challenge1b_input.json      # Input config for Travel Planner persona
│   └── challenge1b_output.json     # Generated output with extracted sections
├── Collection 2/                    # Adobe Acrobat Learning Materials  
│   ├── PDFs/                       # 15 Acrobat workflow documents
│   ├── challenge1b_input.json      # Input config for HR Professional persona
│   └── challenge1b_output.json     # Generated output with form-related content
├── Collection 3/                    # Recipe and Cooking Documents
│   ├── PDFs/                       # 9 recipe and cooking guide PDFs
│   ├── challenge1b_input.json      # Input config for Food Contractor persona
│   └── challenge1b_output.json     # Generated output with recipe content
├── utils/
│   └── parser.py                   # PDF text extraction utilities
├── src/                            # Additional source modules (if any)
├── pdf_process.py                  # Main processing script
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
└── README.md                       # This documentation
```

---

## 🔧 Technical Implementation

### Core Components

1. **PDF Processing Engine** (`utils/parser.py`)
   - Text extraction from PDF documents
   - Page-level content organization
   - Structured data formatting

2. **Persona Analysis System** (`pdf_process.py`)
   - Role-based content filtering
   - Task-specific relevance scoring
   - Context-aware section extraction

3. **Output Generation** 
   - Standardized JSON format
   - Metadata collection and analysis
   - Section ranking and selection

### Key Features

- ✅ **Multi-Domain Support**: Travel guides, HR documents, recipe collections
- ✅ **Persona-Aware Processing**: Tailored extraction based on user roles
- ✅ **Structured Output**: Consistent JSON format with rich metadata
- ✅ **Docker Ready**: Containerized for easy deployment
- ✅ **Efficient Processing**: Optimized for quick batch processing

---

## 📋 Supported Personas & Use Cases

| Persona | Domain | Focus Areas | Sample Tasks |
|---------|--------|-------------|-------------|
| **Travel Planner** | Tourism & Travel | Itineraries, destinations, cultural insights | Plan group trips, find attractions, discover local cuisine |
| **HR Professional** | Human Resources | Forms, workflows, compliance | Automate onboarding, digital signatures, document management |
| **Food Contractor** | Culinary & Catering | Recipes, nutrition, large-scale preparation | Menu planning, vegetarian options, catering logistics |

---

## 📥 Input Configuration

Each collection contains a `challenge1b_input.json` file:

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {
      "filename": "South of France - Cities.pdf",
      "title": "South of France - Cities"
    },
    {
      "filename": "South of France - Cuisine.pdf", 
      "title": "South of France - Cuisine"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan comprehensive itinerary for college group visiting France"
  }
}
```

---

## 📤 Output Format

Generated `challenge1b_output.json` files contain:

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan comprehensive itinerary..."
  },
  "extracted_sections": [
    {
      "document": "South of France - Cities.pdf",
      "section_title": "South of France - Cities", 
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cities.pdf",
      "refined_text": "France offers diverse cultural experiences...",
      "page_number": 1
    }
  ]
}
```
# Challenge 1B: Persona-Driven Document Intelligence

## Approach Explanation

### Overview

Our solution implements a sophisticated persona-driven document intelligence system that processes multiple PDF collections and extracts the most relevant content based on specific user personas and their job-to-be-done requirements. The system handles three distinct collections: Travel Planning, Adobe Acrobat Learning, and Recipe Collections.

### Core Architecture

#### 1. PDF Processing Pipeline (PDFProcessor)

The foundation of our system provides robust document analysis:

- **Multi-format Text Extraction**: Uses PyMuPDF for comprehensive PDF text extraction with page-level granularity
- **Intelligent Section Detection**: Implements pattern-based header recognition using regex patterns for titles, numbered sections, and structural elements
- **Content Quality Assessment**: Filters and validates extracted sections based on length, coherence, and structural integrity
- **Error Handling**: Graceful failure management for corrupted or inaccessible PDF files

#### 2. Persona Analysis Engine (PersonaAnalyzer)

The core intelligence component that understands user context:

- **Dynamic Persona Classification**: Automatically identifies persona types (Travel Planner, HR Professional, Food Contractor) from role descriptions
- **Domain-Specific Keyword Matching**: Maintains specialized vocabularies for each persona category
- **Job Context Integration**: Analyzes job-to-be-done descriptions to enhance relevance scoring
- **Weighted Scoring Algorithm**: Combines persona-specific and task-specific relevance with configurable weights (60% persona, 40% task)

#### 3. Content Relevance Scoring

Advanced algorithmic approach for content prioritization:

- **Multi-dimensional Analysis**: Evaluates content against both persona keywords and job-specific terminology
- **Frequency-based Scoring**: Calculates keyword density while normalizing for content length
- **Amplified Differentiation**: Uses scoring amplification (15x multiplier) to create clear relevance distinctions
- **Bounded Output**: Caps relevance scores at 1.0 for consistent comparison

### Technical Implementation Details

#### Collection Processing Workflow

1. **Input Configuration Loading**: Parses `challenge1b_input.json` files for each collection
2. **Document Iteration**: Processes all PDFs in collection-specific directories
3. **Section Extraction**: Applies persona-aware analysis to each document section
4. **Relevance Ranking**: Sorts content by calculated relevance scores
5. **Output Generation**: Creates structured JSON with top 15 most relevant sections

#### Performance Optimizations

- **Streaming Processing**: Handles large document collections without memory overflow
- **Content Length Limiting**: Truncates section content to 1000 characters for output efficiency
- **Early Filtering**: Removes low-quality sections before expensive scoring operations
- **Batch Processing**: Efficiently processes all three collections in sequence

### Persona-Specific Adaptations

#### Travel Planner Persona

- **Keywords**: destination, itinerary, accommodation, restaurant, attraction, activity, budget, transportation, booking, schedule, group, hotel, tourism, sightseeing, culture, history, local, france, travel, trip, vacation, guide, tourist, city, cuisine
- **Focus Areas**: Group planning, budget considerations, local experiences, cultural insights

#### HR Professional Persona

- **Keywords**: form, document, compliance, onboarding, employee, policy, signature, workflow, process, digital, fillable, field, data, collection, management, automation, electronic, acrobat, pdf, create, convert, edit, export, fill, sign
- **Focus Areas**: Digital workflows, form creation, compliance management, automation

#### Food Contractor Persona

- **Keywords**: recipe, ingredient, cooking, preparation, menu, dish, vegetarian, buffet, serving, nutrition, meal, kitchen, catering, corporate, dinner, food, cuisine, dietary, breakfast, lunch, restaurant, chef, cooking
- **Focus Areas**: Menu planning, dietary restrictions, corporate catering, buffet-style serving

### Innovation Highlights

- **Context-Aware Processing**: Adapts analysis approach based on document collection characteristics
- **Multi-Collection Intelligence**: Handles diverse document types with tailored processing strategies
- **Scalable Architecture**: CPU-only design suitable for production deployment
- **Comprehensive Output**: Provides detailed metadata, processing statistics, and analytical insights

### Quality Assurance

- **Schema Compliance**: Strict adherence to required JSON output format
- **Error Recovery**: Robust handling of missing files and processing failures
- **Performance Monitoring**: Detailed logging and processing statistics
- **Validation Framework**: Built-in checks for output quality and completeness
- **Intelligent Diversification**: Balances relevance with content variety
- **Scalable Architecture**: Handles diverse domains and persona types without manual configuration

This approach ensures high-quality, persona-specific content extraction while maintaining performance constraints and schema compliance requirements.

---

## 🚀 How to Run

### Method 1: Python Direct Execution

```bash
# Navigate to project directory
cd challange_1b

# Install dependencies
pip install -r requirements.txt

# Run the processor
python pdf_process.py
```

### Method 2: Docker Container (Recommended)

```bash
# Build the Docker image
docker build -t pdf-analysis:1 .

# Run with volume mounting (for file access)
docker run --rm -v "$(pwd):/app" --network none pdf-analysis:1

# For Windows PowerShell:
docker run --rm -v "${PWD}:/app" --network none pdf-analysis:1
```

### Method 3: Docker with Custom Mounting

```bash
# Mount specific directories
docker run --rm \
  -v "/path/to/challange_1b:/app" \
  --network none \
  pdf-analysis:1
```

---

## 📊 Processing Results

After successful execution, you'll see:

```
Processing Collection 1
Output written to Collection 1/challenge1b_output.json

Processing Collection 2  
Output written to Collection 2/challenge1b_output.json

Processing Collection 3
Output written to Collection 3/challenge1b_output.json
```

Each collection will have its corresponding output JSON file with:
- ✅ Extracted sections ranked by relevance
- ✅ Metadata about processed documents
- ✅ Subsection analysis with refined text
- ✅ Persona-specific insights

---

## 🔍 Validation & Testing

### Quick Verification

1. **Check Output Files**: Ensure each collection has `challenge1b_output.json`
2. **Validate JSON Structure**: Confirm proper formatting and required fields
3. **Review Content**: Verify extracted sections match persona requirements
4. **Performance Check**: Monitor processing time and resource usage

### Expected Performance

- ⚡ **Processing Time**: 2-5 seconds per collection
- 💾 **Memory Usage**: < 500MB during execution
- 📁 **Output Size**: Structured JSON with relevant sections
- 🔧 **Compatibility**: Works on CPU-only environments

---

## 🛠️ Dependencies

```txt
PyMuPDF>=1.23.0    # PDF text extraction
json                # Built-in JSON handling
os                  # File system operations
```

---

## 🐳 Docker Configuration

The included `Dockerfile` provides:
- **Base Image**: `python:3.10-slim` for optimal size
- **Platform**: `linux/amd64` for compatibility
- **Dependencies**: Automatic installation from `requirements.txt`
- **Entry Point**: Direct execution of `pdf_process.py`
- **Network**: Isolated execution with `--network none`

---

## 📚 Additional Notes

### Security Features
- Network isolation during Docker execution
- Read-only PDF processing
- No external API dependencies
- Local-only file operations

### Extensibility
- Modular design for adding new personas
- Configurable extraction parameters
- Support for additional document formats
- Scalable to larger document collections

---

## 📄 License

This project is developed for educational and research purposes as part of the Adobe Challenge series.

---

**🎯 Ready to process your document collections with persona-driven intelligence!**
