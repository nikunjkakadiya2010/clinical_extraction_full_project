from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    """
    Extracts text from each page of a PDF using pypdf.
    Returns a list of:
        {
            "page_number": int,
            "text": string
        }
    """

    pages_output = []

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Error reading PDF '{pdf_path}': {e}")

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = ""
            print(f"[WARN] Failed to extract text from page {i+1}: {e}")

        pages_output.append({
            "page_number": i + 1,
            "text": text
        })

    return pages_output
