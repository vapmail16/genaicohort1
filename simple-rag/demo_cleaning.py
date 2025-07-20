#!/usr/bin/env python3
"""
Demonstration of Text Cleaning Preprocessing on Ingested Documents
"""

import os
from pypdf import PdfReader
from simple_text_cleaner import create_simple_text_cleaner
from config import REMOVE_STOPWORDS, REMOVE_NUMBERS

def load_pdf_text(file_path):
    """Load text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def demo_cleaning():
    """Demonstrate text cleaning on actual ingested documents."""
    
    print("🧪 TEXT CLEANING PREPROCESSING DEMONSTRATION")
    print("=" * 60)
    
    # Initialize text cleaner with current config
    cleaner = create_simple_text_cleaner(remove_numbers=REMOVE_NUMBERS)
    
    print(f"📋 Configuration:")
    print(f"   - Remove Stopwords: {REMOVE_STOPWORDS}")
    print(f"   - Remove Numbers: {REMOVE_NUMBERS}")
    print()
    
    # Load and process each PDF in the data directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"❌ Data directory '{data_dir}' not found!")
        return
    
    pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found in '{data_dir}'!")
        return
    
    for pdf_file in pdf_files:
        file_path = os.path.join(data_dir, pdf_file)
        print(f"📄 Processing: {pdf_file}")
        print("-" * 40)
        
        # Load original text
        original_text = load_pdf_text(file_path)
        if not original_text:
            continue
        
        # Take a sample of the text (first 1000 characters)
        sample_size = 1000
        original_sample = original_text[:sample_size]
        
        print(f"📝 ORIGINAL TEXT SAMPLE ({len(original_sample)} chars):")
        print("=" * 50)
        print(repr(original_sample))
        print()
        
        # Clean the text
        cleaned_text = cleaner.clean_text(original_sample, remove_stopwords=REMOVE_STOPWORDS)
        
        print(f"✨ CLEANED TEXT SAMPLE ({len(cleaned_text)} chars):")
        print("=" * 50)
        print(repr(cleaned_text))
        print()
        
        # Show statistics
        print(f"📊 CLEANING STATISTICS:")
        print(f"   - Original length: {len(original_sample)} characters")
        print(f"   - Cleaned length: {len(cleaned_text)} characters")
        print(f"   - Reduction: {len(original_sample) - len(cleaned_text)} characters")
        print(f"   - Reduction %: {((len(original_sample) - len(cleaned_text)) / len(original_sample) * 100):.1f}%")
        print()
        
        # Show specific cleaning examples
        print("🔍 SPECIFIC CLEANING EXAMPLES:")
        print("=" * 50)
        
        # Find examples of HTML-like patterns
        html_examples = []
        for i in range(0, len(original_sample) - 20, 100):
            chunk = original_sample[i:i+20]
            if '<' in chunk and '>' in chunk:
                html_examples.append(chunk)
        
        if html_examples:
            print("   HTML Tags Found:")
            for example in html_examples[:3]:  # Show first 3 examples
                print(f"     Before: {repr(example)}")
                cleaned_example = cleaner.remove_html_tags(example)
                print(f"     After:  {repr(cleaned_example)}")
            print()
        
        # Find examples of special characters
        special_char_examples = []
        for i in range(0, len(original_sample) - 30, 50):
            chunk = original_sample[i:i+30]
            if any(char in chunk for char in '@#$%^&*()_+-=[]{}|;:,.<>?'):
                special_char_examples.append(chunk)
        
        if special_char_examples:
            print("   Special Characters Found:")
            for example in special_char_examples[:3]:  # Show first 3 examples
                print(f"     Before: {repr(example)}")
                cleaned_example = cleaner.clean_special_characters(example)
                print(f"     After:  {repr(cleaned_example)}")
            print()
        
        # Find examples of irregular whitespace
        whitespace_examples = []
        for i in range(0, len(original_sample) - 40, 80):
            chunk = original_sample[i:i+40]
            if '  ' in chunk or '\n\n' in chunk or '\t' in chunk:
                whitespace_examples.append(chunk)
        
        if whitespace_examples:
            print("   Irregular Whitespace Found:")
            for example in whitespace_examples[:2]:  # Show first 2 examples
                print(f"     Before: {repr(example)}")
                cleaned_example = cleaner.normalize_whitespace(example)
                print(f"     After:  {repr(cleaned_example)}")
            print()
        
        # Show case conversion example
        if original_sample:
            print("   Case Conversion:")
            print(f"     Before: {repr(original_sample[:100])}")
            print(f"     After:  {repr(original_sample[:100].lower())}")
            print()
        
        print("=" * 60)
        print()

def demo_cleaning_steps():
    """Demonstrate each cleaning step individually."""
    
    print("🔧 INDIVIDUAL CLEANING STEPS DEMONSTRATION")
    print("=" * 60)
    
    # Sample text with various issues
    sample_text = """
    <p>This is a <strong>sample</strong> text with HTML tags.</p>
    It contains numbers like 123 and 456.7, and special characters @#$%.
    The text has multiple    spaces and
    newlines.
    Some UPPERCASE and lowercase text mixed together.
    """
    
    cleaner = create_simple_text_cleaner(remove_numbers=False)
    
    print("📝 ORIGINAL TEXT:")
    print(repr(sample_text))
    print()
    
    # Step 1: HTML tag removal
    step1 = cleaner.remove_html_tags(sample_text)
    print("1️⃣ HTML TAG REMOVAL:")
    print(repr(step1))
    print()
    
    # Step 2: Special character cleaning
    step2 = cleaner.clean_special_characters(step1)
    print("2️⃣ SPECIAL CHARACTER CLEANING:")
    print(repr(step2))
    print()
    
    # Step 3: Whitespace normalization
    step3 = cleaner.normalize_whitespace(step2)
    print("3️⃣ WHITESPACE NORMALIZATION:")
    print(repr(step3))
    print()
    
    # Step 4: Lowercase conversion
    step4 = step3.lower()
    print("4️⃣ LOWERCASE CONVERSION:")
    print(repr(step4))
    print()
    
    # Step 5: Final result
    final = cleaner.clean_text(sample_text, remove_stopwords=False)
    print("🎯 FINAL CLEANED RESULT:")
    print(repr(final))
    print()

if __name__ == "__main__":
    print("🚀 Starting Text Cleaning Demonstration...")
    print()
    
    # Demo individual steps
    demo_cleaning_steps()
    
    # Demo on actual ingested files
    demo_cleaning()
    
    print("✅ Demonstration complete!")
    print("\n💡 Key Benefits of Text Cleaning:")
    print("   - Better semantic matching")
    print("   - Consistent embeddings")
    print("   - Reduced noise in search")
    print("   - Improved LLM responses") 