from django.urls import path

from . import views


urlpatterns = [

    path("",views.dashboard,name="dashboard"),
    path("extract/",views.extract_invoice,name="extract_invoice"),
    path("invoices/",views.invoice_list,name="invoice_list"),
    path("invoice/<int:invoice_id>/pdf/",views.download_pdf,name="download_pdf"),
    path("invoice/<int:invoice_id>/result/",views.download_result,name="download_result"),
    path("invoice/<int:invoice_id>/delete/",views.delete_invoice,name="delete_invoice"),
    path("report/",views.download_report,name="download_report"),

]