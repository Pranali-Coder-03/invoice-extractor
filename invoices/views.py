import io
import pandas as pd

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import HttpResponse
from django.http import (
    HttpResponse,
    FileResponse
)
from .models import Invoice

from .services import (
    upload_to_supabase,
    download_from_supabase,
    delete_from_supabase,
    extract_pdf_text,
    extract_field
)



def dashboard(request):

    total_invoices = Invoice.objects.count()

    extracted_invoices = Invoice.objects.exclude(
        extracted_value__isnull=True
    ).exclude(
        extracted_value=""
    ).count()

    return render(
        request,
        "invoices/dashboard.html",
        {
            "total_invoices": total_invoices,
            "extracted_invoices": extracted_invoices,
            "total_reports": total_invoices,
        }
    )


def extract_invoice(request):

    if request.method == "POST":


        files = request.FILES.getlist(
            "invoice_files"
        )
        

        custom_field = request.POST.get(
            "custom_field",
            ""
        ).strip()


        if not files:

            return render(
                request,
                "invoices/extract.html",
                {
                    "error": "Please select at least one PDF file."
                }
            )


        if not custom_field:

            return render(
                request,
                "invoices/extract.html",
                {
                    "error": "Please enter the field you want to extract."
                }
            )

        processed_count = 0

        for uploaded_file in files:


            if not uploaded_file.name.lower().endswith(
                ".pdf"
            ):
                continue

            try:


                storage_path = upload_to_supabase(
                    uploaded_file
                )


                pdf_bytes = download_from_supabase(
                    storage_path
                )


                text = extract_pdf_text(
                    pdf_bytes
                )


                value = extract_field(
                    text,
                    custom_field
                )

                Invoice.objects.create(

                    original_filename=(
                        uploaded_file.name
                    ),

                    storage_path=(
                        storage_path
                    ),

                    extracted_field=(
                        custom_field
                    ),

                    extracted_value=(
                        value
                    )
                )

                processed_count += 1

            except Exception as e:

                print(
                    f"Error processing "
                    f"{uploaded_file.name}: {e}"
                )

                continue


        if processed_count == 0:

            return render(
                request,
                "invoices/extract.html",
                {
                    "error": (
                        "No PDF invoices could be processed. "
                        "Please check your files and try again."
                    )
                }
            )

        return redirect(
            "invoice_list"
        )


    return render(
        request,
        "invoices/extract.html"
    )


def invoice_list(request):

    invoices = Invoice.objects.all().order_by(
        "-uploaded_at"
    )

    return render(
        request,
        "invoices/invoices.html",
        {
            "invoices": invoices
        }
    )



def download_pdf(
    request,
    invoice_id
):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )


    pdf_bytes = download_from_supabase(
        invoice.storage_path
    )

    response = HttpResponse(
        pdf_bytes,
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'inline; '
        f'filename="{invoice.original_filename}"'
    )

    return response


def delete_invoice(
    request,
    invoice_id
):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )


    if request.method == "POST":

        try:

            # Delete PDF from Supabase Storage

            delete_from_supabase(
                invoice.storage_path
            )

        except Exception as e:

            print(
                f"Supabase delete error: {e}"
            )

        # Delete database record

        invoice.delete()

    return redirect(
        "invoice_list"
    )


def download_result(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )


    fields = [
        field.strip()
        for field in invoice.extracted_field.split(",")
        if field.strip()
    ]


    raw_values = invoice.extracted_value or ""

    values = [
        value.strip()
        for value in raw_values.splitlines()
        if value.strip()
    ]


    lines = []

    lines.append(
        f"Invoice: {invoice.original_filename}"
    )

    lines.append("")

    lines.append(
        "EXTRACTED DATA"
    )

    lines.append(
        "---------------"
    )


    for index, field in enumerate(fields):

        if index < len(values):

            value = values[index]

        else:

            value = "Not found"


        value = value.rstrip(".,;:")

        lines.append(
            f"{field}: {value}"
        )

    lines.append("")

    lines.append(
        f"Uploaded At: {invoice.uploaded_at}"
    )


    content = "\n".join(lines)

    response = HttpResponse(
        content,
        content_type="text/plain"
    )

    response["Content-Disposition"] = (
        f'attachment; '
        f'filename="result_{invoice.id}.txt"'
    )

    return response


def download_report(request):

    invoices = Invoice.objects.all().order_by(
        "-uploaded_at"
    )

    data = []

    for invoice in invoices:

        data.append(
            {
                "Invoice": invoice.original_filename,

                "Field Extracted": invoice.extracted_field,

                "AI Result": invoice.extracted_value,

                "Uploaded At": invoice.uploaded_at,
            }
        )

    df = pd.DataFrame(data)

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Invoice Results"
        )

    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="invoice_report.xlsx"'
    )

    return response