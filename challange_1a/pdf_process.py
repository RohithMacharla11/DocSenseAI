import fitz  # PyMuPDF
import json
import os
import spacy
import re
from collections import defaultdict
import logging
from pathlib import Path
from typing import Union, List, Dict  # For Python 3.9 compatibility

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/pdf_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model 'en_core_web_sm' not found. Install it offline using: python -m spacy download en_core_web_sm")
    raise

def is_heading_text(text: str, font_size: float, is_bold: bool, is_italic: bool, spans: list, in_toc_context: bool) -> bool:
    """
    Determine if text is a heading based on NLP and formatting characteristics.
    Excludes 'table of contents' and its numbered sub-entries when in TOC context.
    """
    if not text.strip():
        return False
    if len(text) > 100:  # Exclude headings longer than 100 characters
        return False

    # Calculate is_numbered early to prevent headings like "1. Introduction..." from being filtered out
    is_numbered = bool(re.match(r'^\s*(Phase\s+[IVXLC]+:|\d+\.\d*(\.\d+)*\s)', text, re.IGNORECASE) or re.match(r'^\s*[A-Z]\.\s', text))

    # Apply span check only to non-numbered headings
    if not is_numbered and len(spans) > 1 and not (is_bold or is_italic):
        return False

    if text.strip().lower() == "table of contents":
        return False
    # Exclude numbered entries if in TOC context
    if in_toc_context and re.match(r'^\s*\d+\.\s', text):
        return False
    doc = nlp(text)
    is_short = len(doc) < 12
    is_title_case = sum(1 for token in doc if token.text[0].isupper()) > len(doc) / 2
    
    return is_numbered or (is_short and (is_bold or font_size > 10)) or (is_title_case and font_size > 10 and not is_italic)

def clean_title(text: str) -> str:
    """
    Clean the title text to make it meaningful.
    """
    text = re.sub(r'[-]{2,}', ' ', text)
    text = re.sub(r'(\w+)\s+\1', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s-]$', '', text)
    return text if text else "Untitled"

def extract_headings(pdf_path: str) -> tuple[Union[str, None], List[Dict]]:
    """
    Extract title and hierarchical headings (H1, H2, H3) from a PDF file.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"Failed to open PDF {pdf_path}: {e}")
        return None, []
    
    outline = []
    title = None
    toc_context = {}  # Track TOC context per page
    
    for page_num, page in enumerate(doc, 1):
        try:
            blocks = page.get_text("blocks", sort=True)
            if not blocks:
                continue
            
            if page_num == 1 and not title:
                try:
                    bold_blocks = [b for b in blocks if b[6] == 0 and any(page.get_text("dict", clip=b[:4]).get("blocks", [{}])[0].get("lines", [{}])[0].get("spans", [{}])[0].get("flags", 0) & 16 for s in page.get_text("dict", clip=b[:4]).get("blocks", [{}])[0].get("lines", [{}])[0].get("spans", []))]
                    if bold_blocks:
                        title_block = max(bold_blocks, key=lambda x: max(s.get("size", 0) for s in page.get_text("dict", clip=x[:4]).get("blocks", [{}])[0].get("lines", [{}])[0].get("spans", [])))
                        title = clean_title(title_block[4].strip().replace('\n', ' '))
                        # logger.info(f"Title detected from bold block: {title}")
                    else:
                        # logger.info("No bold blocks found, trying largest font size")
                        all_blocks = [b for b in blocks if b[6] == 0 and len(b[4].split()) > 1 and not re.search(r'[-]{5,}', b[4])]
                        if all_blocks:
                            title_block = max(all_blocks, key=lambda x: max(s.get("size", 0) for s in page.get_text("dict", clip=x[:4]).get("blocks", [{}])[0].get("lines", [{}])[0].get("spans", [])))
                            title = clean_title(title_block[4].strip().replace('\n', ' '))
                            # logger.info(f"Title detected from largest font size: {title}")
                        else:
                            logger.info("No valid blocks with font size, using first meaningful block")
                            first_block = next((b for b in blocks if b[6] == 0 and len(b[4].split()) > 1 and not re.search(r'[-]{5,}', b[4])), None)
                            title = clean_title(first_block[4].strip().replace('\n', ' ') if first_block else "Untitled")
                            # logger.info(f"Title fallback to first block: {title}")
                except Exception:
                    first_block = next((b for b in blocks if b[6] == 0 and len(b[4].split()) > 1 and not re.search(r'[-]{5,}', b[4])), None)
                    title = clean_title(first_block[4].strip().replace('\n', ' ') if first_block else "Untitled")
                continue
            
            lines = defaultdict(list)
            for block in blocks:
                if block[6] != 0:
                    continue
                y_coord = round(block[1], 1)
                lines[y_coord].append(block)
            
            toc_detected = False
            toc_subentry_count = toc_context.get(page_num, {}).get('count', 0)  # Track numbered lines after TOC
            for y, block_list in sorted(lines.items()):
                line_text = " ".join(b[4].strip().replace('\n', ' ') for b in block_list).strip()
                if not line_text:
                    continue
                
                try:
                    dict_text = page.get_text("dict", clip=block_list[0][:4])
                    spans = dict_text.get("blocks", [{}])[0].get("lines", [{}])[0].get("spans", [])
                    font_info = spans[0] if spans else {"size": 12, "flags": 0}
                    font_size = font_info.get("size", 12)
                    is_bold = font_info.get("flags", 0) & 16 or 'bold' in font_info.get("font", "").lower()
                    is_italic = font_info.get("flags", 0) & 2 or 'italic' in font_info.get("font", "").lower()
                    
                    # Update TOC context
                    if line_text.strip().lower() == "table of contents":
                        toc_detected = True
                        toc_context[page_num] = {'active': True, 'count': 0}
                        continue
                    
                    if is_heading_text(line_text, font_size, is_bold, is_italic, spans, toc_context.get(page_num, {}).get('active', False)) and block_list[0][0] < page.rect.width / 4:
                        if not outline or (font_size >= 18 and is_bold and len(line_text.split()) < 10):
                            level = "H1"
                            # Reset TOC context when a new H1 is detected
                            if page_num in toc_context:
                                toc_context[page_num]['active'] = False
                        elif 12 <= font_size < 18:
                            level = "H2"
                        elif (10.5 <= font_size < 12 and len(line_text.split()) < 10) or \
                             re.match(r'^\s*Phase\s+[IVXLC]+\s*:', line_text, re.IGNORECASE) or \
                             (re.match(r'^\s*\d+\.\s', line_text) and (is_bold or is_italic)) or \
                             (re.match(r'^\s*\d+\.\s', line_text) and not re.search(r'\d\.\d', line_text) and len(line_text.split()) < 5 and is_bold):
                            level = "H3"
                        else:
                            continue
                        
                        outline.append({
                            "level": level,
                            "text": line_text,
                            "page": page_num
                        })
                        # Increment and limit TOC subentry count
                        if toc_detected and re.match(r'^\s*\d+\.\s', line_text) and len(line_text.split()) < 10:
                            toc_subentry_count += 1
                            toc_context[page_num] = {'active': True, 'count': toc_subentry_count}
                            if toc_subentry_count >= 5:  # Limit TOC context to first 5 numbered lines
                                toc_context[page_num]['active'] = False
                except Exception as e:
                    logger.warning(f"Error processing line on page {page_num} of {pdf_path}: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Error processing page {page_num} of {pdf_path}: {e}")
    
    doc.close()
    return title, outline

def process_pdfs(input_dir: str, output_dir: str) -> None:
    """
    Process all PDFs from input_dir and save outlines to output_dir as JSON.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        logger.error(f"Input directory {input_dir} does not exist")
        return
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    for pdf_file in input_path.glob("*.pdf"):
        logger.info(f"Processing {pdf_file.name}")
        try:
            title, outline = extract_headings(str(pdf_file))
            if title or outline:
                output = {
                    "title": title or "",
                    "outline": outline
                }
                output_file = output_path / pdf_file.with_suffix('.json').name
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                logger.info(f"Successfully processed {pdf_file.name}")
            else:
                logger.info(f"No title or headings detected in {pdf_file.name}")
        except Exception as e:
            logger.error(f"Error processing {pdf_file.name}: {e}")

if __name__ == "__main__":
    process_pdfs("./app/input", "./app/output")