import streamlit as st
from docx import Document
import re
from collections import Counter

def extract_text_from_docx(file):
    """Extracts text from a .docx file, excluding the reference section."""
    doc = Document(file)
    full_text = []
    in_reference_section = False

    for para in doc.paragraphs:
        # Check for the start of the reference section
        if 'References' in para.text or 'References:' in para.text:
            in_reference_section = True
            continue  # Skip the reference section header
        
        if in_reference_section:
            continue  # Skip all text after the reference section

        full_text.append(para.text)
    
    return '\n'.join(full_text)

def find_names_and_years(text):
    """Find all instances of 'Name (Year)' in the text."""
    # Adjust the regex pattern as needed to capture names and years
    pattern = r'([A-Z][a-zA-Z]+) \((\d{4})\)'
    matches = re.findall(pattern, text)
    return matches

def check_citations(names_and_years):
    """Count occurrences of names and determine if they are cited or uncited."""
    counts = Counter(names_and_years)
    uncited = [(name, year) for (name, year), count in counts.items() if count == 1]
    return uncited

# Streamlit UI
st.title("Uncited Reference Checker")

uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

if uploaded_file is not None:
    text = extract_text_from_docx(uploaded_file)
    names_and_years = find_names_and_years(text)

    # Create a list of names and years
    name_years = [(name, year) for name, year in names_and_years]

    # Check for uncited references
    uncited_references = check_citations(name_years)

    if uncited_references:
        st.subheader("Uncited References Found:")
        for name, year in uncited_references:
            st.write(f"{name} ({year}) - Mentioned 1 time(s) (Uncited)")
    else:
        st.write("No uncited references found.")
