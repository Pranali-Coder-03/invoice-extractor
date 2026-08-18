import os
import uuid

import fitz

from supabase import create_client
from google import genai


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

BUCKET = "invoices"


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def upload_to_supabase(uploaded_file):

    extension = os.path.splitext(
        uploaded_file.name
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    path = f"invoices/{filename}"

    file_bytes = uploaded_file.read()

    supabase.storage \
        .from_(BUCKET) \
        .upload(
            path,
            file_bytes,
            {
                "content-type": "application/pdf"
            }
        )

    return path


def download_from_supabase(path):

    return (
        supabase
        .storage
        .from_(BUCKET)
        .download(path)
    )


def delete_from_supabase(path):

    return (
        supabase
        .storage
        .from_(BUCKET)
        .remove([path])
    )


def extract_pdf_text(pdf_bytes):

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:

        text += page.get_text()

        text += "\n"

    document.close()

    return text


def extract_field(pdf_text, field):

    prompt = f"""
You are an invoice data extraction system.

Extract ONLY the requested field from the invoice.

Requested field:
{field}

Invoice text:
----------------
{pdf_text}
----------------

Rules:

1. Return only the value.
2. Do not explain anything.
3. If the value does not exist, return:
NOT FOUND
4. Understand different labels that mean the same thing.
5. Preserve the original value as much as possible.

Examples:

"Date of Issue" can appear as:
Invoice Date
Issue Date
Date Issued
Issued On
Invoice Dt

"Billed To" can appear as:
Bill To
Billed To
Customer
Buyer
Customer Name

Return only the extracted value.
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()