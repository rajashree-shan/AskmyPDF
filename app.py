import gradio as gr
import fitz  # PyMuPDF
import pdfplumber
import re
import os
import tempfile
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- PDF Utilities ---
def extract_text_from_pdf(file_path):
    all_pages = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_pages.append((i + 1, text))
    return all_pages

# --- highlight in PDF ---
def highlight_keyword_in_pdf(file, keyword):
    input_pdf_path = file.name
    doc = fitz.open(input_pdf_path)

    highlights_found = False
    summary = "Keywords found in:<br>"

    for page_num, page in enumerate(doc, start=1):
        words = page.get_text("words")
        found_on_page = False

        for w in words:
            word_text = w[4]
            if keyword.lower() in word_text.lower():
                found_on_page = True
                highlights_found = True

                rect = fitz.Rect(w[0], w[1], w[2], w[3])
                highlight = page.add_highlight_annot(rect)
                highlight.update()

        if found_on_page:
            # Collect lines for summary text
            page_text = page.get_text()
            lines = page_text.split('\n')
            matching_lines = [
                line for line in lines if keyword.lower() in line.lower()
            ]
            summary += f"<br><b>Page {page_num}:</b><br>"
            for line in matching_lines:
                # Highlight keyword in summary text using HTML <mark>
                highlighted_line = re.sub(
                    f"({re.escape(keyword)})",
                    r"<mark>\1</mark>",
                    line,
                    flags=re.IGNORECASE
                )
                summary += f"{highlighted_line}<br>"

    temp_dir = tempfile.mkdtemp()
    output_pdf_path = os.path.join(temp_dir, "highlighted.pdf")
    doc.save(output_pdf_path)

    if highlights_found:
        message = summary
    else:
        message = "No occurrences of the keyword found."

    return message, output_pdf_path

# --- Semantic Q&A ---
def semantic_qa(file, question):
    if not question.strip():
        return "Please enter a question."

    pages = extract_text_from_pdf(file.name)
    combined_text = "\n\n".join([f"Page {num}:\n{text}" for num, text in pages])
    truncated_text = combined_text[:3000]

    messages = [
        {"role": "system", "content": "You are an expert assistant helping summarize and answer questions about a PDF document."},
        {"role": "user", "content": f"The following text is extracted from a PDF:\n\n{truncated_text}\n\nQuestion: {question}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

with gr.Blocks(title="PDF Assistant: Highlight + Semantic Q&A") as demo:
    gr.Markdown(
        """
        # PDF Assistant
        Upload a PDF, highlight keywords inside the PDF file itself, and ask semantic questions using OpenAI GPT.
        - **PDF Highlight:** Finds,highlights keyword occurrences across pages and creates a new PDF file with highlights for your keyword.
        - **Semantic Q&A:** Ask a natural language question about PDF content.
        """
    )

    with gr.Tab("PDF Highlighter"):
        file_input_highlight = gr.File(label="Upload PDF", file_types=[".pdf"])
        keyword_input = gr.Textbox(label="Keyword to highlight")
        highlight_btn = gr.Button("Highlight in PDF")
        highlight_message = gr.HTML()
        highlighted_pdf_output = gr.File(label="Download highlighted PDF")

        highlight_btn.click(
            fn=highlight_keyword_in_pdf,
            inputs=[file_input_highlight, keyword_input],
            outputs=[highlight_message, highlighted_pdf_output]
        )

    with gr.Tab("Semantic Q&A"):
        file_input_qa = gr.File(label="Upload PDF", file_types=[".pdf"])
        question_input = gr.Textbox(label="Ask a question about this PDF")
        ask_btn = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer", lines=6)

        ask_btn.click(
            fn=semantic_qa,
            inputs=[file_input_qa, question_input],
            outputs=answer_output
        )

demo.launch()