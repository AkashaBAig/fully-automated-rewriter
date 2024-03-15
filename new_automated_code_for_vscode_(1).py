import openai
import PyPDF2
from fpdf import FPDF
import os
import pytesseract
from PIL import Image
import pandas as pd
import io

import PyPDF2

file_path = "setupthree.pdf"  # Use the correct file path

# Open the file in binary mode and create a PDF reader object
with open(file_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"  # Extract text from each page

print(text)  # Now you can work with the extracted text

import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Path to your uploaded PDF
pdf_path = "setupthree.pdf"
text = extract_text_from_pdf(pdf_path)
print(text)

import os
import subprocess
from pdf2image import convert_from_path

def extract_images_from_pdf(pdf_path, print_images=False):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image_path = f'sys_image_{i}.jpg'
        image.save(image_path, 'JPEG')

        if print_images:
            # Print the image using the default system printer
            os_command = f'lpr {image_path}'
            subprocess.run(os_command, shell=True)

# Path to your uploaded PDF
#pdf_path = 'setupthree.pdf'
#extract_images_from_pdf(pdf_path, print_images=True)

import tabula

def extract_tables_from_pdf(pdf_path):
    # Ensure all pages are scanned and multiple tables are extracted
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, lattice=True)

    # Save each extracted table as a CSV file
    for i, table in enumerate(tables):
        table.to_csv(f'sys_table_{i}.csv', index=False)

# Path to your uploaded PDF
#pdf_path = 'setupthree.pdf'
#extract_tables_from_pdf(pdf_path)

# Set your OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = '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'

import openai
import os

# Retrieve the OpenAI API key from the environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

# New function to extract text from images using OCR
def extract_text_from_images(images):
    ocr_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        ocr_text += text + "\n\n"
    return ocr_text

# New function to convert tables to text
def tables_to_text(tables):
    tables_text = ""
    for table in tables:
        output = io.StringIO()
        table.to_csv(output)
        tables_text += output.getvalue()
        output.close()
    return tables_text

# Modify your rewrite_pdf function to include all texts
def rewrite_pdf(input_pdf_path, prompt):
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(input_pdf_path)

    print("PDF TEXT:",pdf_text)

    # Extract images and OCR text from images
    # images = convert_from_path(input_pdf_path)
    # image_text = extract_text_from_images(images)

    # # Extract tables and convert to text
    # tables = tabula.read_pdf(input_pdf_path, pages='all', multiple_tables=True, lattice=True)
    # tables_text = tables_to_text(tables)

    # Combine all texts
    combined_text = pdf_text + "\n\n" #+ image_text + "\n\n" + tables_text
    combined_text = combined_text.encode('latin-1', 'replace').decode('latin-1')

    # Combine with the prompt
    full_prompt = prompt + "\n\n" + combined_text

    # Get rewritten text from AI model
    # Encode the rewritten_text variable using utf-8
    rewritten_text = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "kindly provide as much detail in relation to the question also share each step that require guidance"},
            {"role": "user", "content": full_prompt},
        ]
     )['choices'][0]['message']['content']

    print("Rewritten Text:",rewritten_text)

    # Save the rewritten text as a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, rewritten_text)
    output_pdf_path = input_pdf_path.replace('.pdf', '_rewritten.pdf')
    pdf.output(output_pdf_path)
    return output_pdf_path

def rewrite_pdfs(input_pdf_path, prompt):
    # Extract text from PDF
    pdf_texts = list_extract_text_from_pdf(input_pdf_path)
    pdf = FPDF()

    for pdf_text in pdf_texts:

      print("PDF TEXT:",pdf_text)


      # Combine all texts
      combined_text = pdf_text + "\n\n" #+ image_text + "\n\n" + tables_text
      combined_text = combined_text.encode('latin-1', 'replace').decode('latin-1')

      # Combine with the prompt
      full_prompt = prompt + "\n\n" + combined_text

      # Get rewritten text from AI model
      # Encode the rewritten_text variable using utf-8
      rewritten_text = openai.ChatCompletion.create(
          model="gpt-4-1106-preview",
          messages=[
              {"role": "system", "content": "kindly provide as much detail in relation to the question also share each step that require guidance"},
              {"role": "user", "content": full_prompt},
              # {"role": "user", "content": combined_text},

          ]
      )['choices'][0]['message']['content']

      print("Rewritten Text:",rewritten_text)
      rewritten_text = rewritten_text.encode('latin-1', 'replace').decode('latin-1')

      # Save the rewritten text as a PDF
      count = 1
      # for x in range(len(pdf_texts)):
      pdf.add_page()
      pdf.set_font("Arial", size=12)
      pdf.multi_cell(0, 10, rewritten_text)
      output_pdf_path = input_pdf_path.replace('.pdf', '_rewritten.pdf')
      pdf.output(output_pdf_path)
      pdf = FPDF()

    return output_pdf_path

import PyPDF2
import io
from reportlab.pdfgen import canvas

def read_pdf_sections(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        sections = [page.extract_text() for page in reader.pages]  # Each page considered as a section
    return sections

def rewrite_section(section_text, rewrite_instructions):
    # Simulate rewriting operation; in reality, this might involve more complex logic or manual editing
    rewritten_section = f"{rewrite_instructions}\n{section_text}"
    return rewritten_section

def rewrite_pdf_interactively(uploaded_pdf_path, rewrite_instructions):
    sections = read_pdf_sections(uploaded_pdf_path)
    all_rewritten_content = ""

    for i, section in enumerate(sections, start=1):
        print(f"original section {i} content:")
        print(section)

        # Simulate rewriting the section according to provided instructions
        rewritten_section = rewrite_section(section, rewrite_instructions)
        print(" rewritten section:")
        print(rewritten_section)

        proceed = input("Do you want to proceed with the next section? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Operation halted. Proceeding to save the content rewritten so far to a PDF.")
            break
        all_rewritten_content += rewritten_section + "\n\n"

    # Saving the rewritten content to a PDF
    output_pdf_path = "rewritten_content.pdf"
    output_stream = io.BytesIO()
    c = canvas.Canvas(output_stream)
    text_object = c.beginText(40, 800)
    text_object.setFont("Times-Roman", 12)
    text_object.textLines(all_rewritten_content)
    c.drawText(text_object)
    c.save()

    with open(output_pdf_path, "wb") as f:
        f.write(output_stream.getvalue())

    print("Rewritten content saved to PDF: " + output_pdf_path)
    return output_pdf_path

uploaded_pdf_path = "setupthree.pdf"
# Example usage
output_pdf = rewrite_pdf(uploaded_pdf_path, "Your task involves rewritting each and every section, the task is to rewrite and simplify all given sections,focusing on one section at a time and rewritting it clearly with more detail.Let's work through each section, one at a time, starting with the first.")

print(f"Rewritten content saved in PDF: {output_pdf}")