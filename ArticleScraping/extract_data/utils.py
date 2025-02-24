import fitz  # PyMuPDF for PDF extraction
import re
import spacy
import pycountry

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def find_country(text):
    """Detect country using NLP and PyCountry."""
    country_candidates = []
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:  # Geopolitical Entity or Location
            for country in pycountry.countries:
                if ent.text.lower() in country.name.lower():
                    country_candidates.append(country.name)

    return country_candidates[0] if country_candidates else "Unknown"

def extract_journal_name(text):
    """Extract journal name using regex and NLP."""
    match = re.search(r"(?i)published in (.*?)[.,]", text)
    if match:
        return match.group(1).strip()

    # Use NLP as a backup
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Organizations often include journal names
            return ent.text

    return "Unknown"

def extract_authors(text):
    """Extract author names using NLP."""
    doc = nlp(text)
    authors = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Try another approach if no authors found
    if not authors:
        author_match = re.search(r"(?i)by\s+([\w\s,]+)", text)
        if author_match:
            authors = [name.strip() for name in author_match.group(1).split(",")]

    return ", ".join(authors[:5]) if authors else "Unknown"

def extract_title(text, doc):
    """Extract the title from PDF metadata or the first few lines."""
    # Try metadata first
    title = doc.metadata.get("title", "").strip()
    if title:
        return title

    # Fallback to first meaningful line (avoiding headers)
    lines = text.split("\n")
    for line in lines:
        if len(line.split()) > 3:  # Avoiding single-word headers
            return line.strip()

    return "Unknown Title"

def extract_abstract(text):
    """Extract an abstract using NLP sentence segmentation."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:5]) if sentences else "Unknown"

def extract_year(text):
    """Extract the publication year using regex with better context handling."""
    match = re.search(r"\b(19|20)\d{2}\b", text)
    if match:
        return match.group()

    return "Unknown"

def extract_article_info(pdf_path):
    """Extract metadata from a given PDF."""
    doc = fitz.open(pdf_path)
    full_text = " ".join([page.get_text("text") for page in doc])

    return {
        "title": extract_title(full_text, doc),
        "abstract": extract_abstract(full_text),
        "year": extract_year(full_text),
        "country": find_country(full_text),
        "journal_name": extract_journal_name(full_text),
        "authors": extract_authors(full_text),
        "article_link": "No link found"
    }
