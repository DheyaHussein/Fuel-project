from django.shortcuts import render
from django.views.generic import ListView
from ..models import StoreHouse
# from weasyprint import HTML
from django.http import HttpResponse
from ..storehouse.utils import generate_storehouse_pdf  # Import the helper function
from django.urls import reverse_lazy
import os
from rest_framework import viewsets
from ..api.serializers import *


from django.conf import settings



# Create your views here.

class StorHouseView(viewsets.ViewSet):
    
    """_summary_
    

    Returns:
        _type_: _description_
    """ 
    queryset = StoreHouse.objects.all()
    
    




class StoreHouseListView(ListView):
    model = StoreHouse
    queryset = StoreHouse.objects.all()
    template_name = 'index.html'
    context_object_name = 'storehouses'
    
    # def get_queryset(self):
        
    #     return super().get_queryset()
    
    # def get(self, request, *args, **kwargs):
    #     if request.GET.get('format') == 'pdf':
    #         self.object_list = self.queryset
    #         context = self.get_context_data()
    #         pdf = generate_storehouse_pdf(self.queryset, context)
    #         if pdf:
    #             response = HttpResponse(pdf, content_type='application/pdf')
    #             response['Content-Disposition'] = 'attachment; filename="storehouse_report.pdf"'
    #             return response
    #         else:
    #             return HttpResponse("Error generating PDF", status=400)
    #     else:
    #         return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Handle PDF generation when the button is pressed
        storehouses = self.queryset

        # Define the file path for the generated PDF
        file_path = os.path.join(settings.MEDIA_ROOT, 'storehouse_report.pdf')

        # Generate the PDF
        generate_storehouse_pdf(storehouses, file_path)

        # Serve the PDF as a download
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="storehouse_report.pdf"'
            return response