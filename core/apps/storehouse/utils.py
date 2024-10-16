# apps/storehouse/utils.py

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from django.conf import settings

from io import BytesIO


# def render_to_pdf(template_src, context_dict={}):
#     """
#     Renders a Django template to PDF.

#     :param template_src: Path to the template.
#     :param context_dict: Context data for the template.
#     :return: PDF byte content or None if error.
#     """
    # template = get_template(template_src)
    # html  = template.render(context_dict)
    # result = io.BytesIO()
    # pisa_status = pisa.CreatePDF(
    #     src=html, dest=result)
    # if pisa_status.err:
    #     return None
    # return result.getvalue()
    
    # template = get_template(template_src)
    # html = template.render(context_dict)
    
    # # Create a file-like buffer to receive PDF data
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="storehouse_report.pdf"'

    # # Use pisa to render the HTML as PDF
    # pisa_status = pisa.CreatePDF(
    #     html, dest=response,
    #     encoding='UTF-8',  # Ensure UTF-8 encoding for Arabic text
    # )
    
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response
def register_fonts():
    """
    Registers the Amiri font with ReportLab.
    """
    amiri_font_path = os.path.join(r'C:\\Users\\USERWD\\Fuel-project\\core\static\\NotoSansArabic.ttf', 'NotoSansArabic.ttf')
    if not os.path.exists(amiri_font_path):
     pdfmetrics.registerFont(TTFont('NotoSansArabic', amiri_font_path))

def reshape_text(text):
    """
    Reshapes Arabic text for correct display.
    
    :param text: Original Arabic text.
    :return: Reshaped text suitable for RTL display.
    """
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def generate_storehouse_pdf(storehouses, file_path):
    """
    Generates a PDF report for StoreHouse instances.
    
    :param storehouses: QuerySet of StoreHouse instances.
    :param file_path: Path where the PDF will be saved.
    """
    # Register fonts
    # register_fonts()
    
    # Create a PDF document
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=18
    )
    
    elements = []
    
    # Define styles
    # styles = getSampleStyleSheet()
    # styles.add(ParagraphStyle(name='Center', alignment=1, fontName='NotoSansArabic'))
    # styles.add(ParagraphStyle(name='Right', alignment=2, fontName='NotoSansArabic'))
    
    # Title
    elements.append(Paragraph('Store Report', encoding='utf8'))
    elements.append(Spacer(1, 12))
    
    # Table data
    data = [
        [
            'الاسم', 
            'اسم المسؤول', 
            'رقم الهاتف', 
            'الموقع'
        ]
    ]
    
    for storehouse in storehouses:
        data.append([
            reshape_text(storehouse.name),
            # reshape_text(storehouse.store_categroy.name),  # Assuming store_categroy is a ForeignKey
            reshape_text(storehouse.storekeeper),
            reshape_text(storehouse.phone_number),
            reshape_text(storehouse.location),
        ])
    
    # Create table
    table = Table(data, repeatRows=1)
    
    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        # ('FONTNAME', (0,0), (-1,-1), 'Center'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)