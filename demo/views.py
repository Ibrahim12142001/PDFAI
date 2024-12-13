from django.shortcuts import render
from django.http import HttpResponse
import demo.models as model
from django.views.generic import CreateView
from pypdf import PdfReader
import pandas as pd
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import os
from io import BytesIO
from django.conf import settings
from azure.identity import DefaultAzureCredential
from django.core.files.storage import default_storage
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
import json
import csv
from django.http import JsonResponse, HttpResponse
import io


# <----------------------------------------------------- Rendering functions ------------------------------------------------------> 

def demo_home(request):
    return render(request, 'demo_home.html')

def banner_image(request):
    image_path = os.path.join(settings.BASE_DIR, 'chatbot', 'banner.jpg')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

class CommonMixin():
    '''
    This is a mixin for all the variables and tools that we expect to have in view
    This should be called after a View class, if possible
    '''

    # key is used to construct commonly formatted strings, such as used in the get_success_url
    key = None

    # title to display on the CreateView page either this var or the h1 var is required
    title = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a java_script file at the bottom of the
    # 'shared_models/shared_entry_form.html' template
    java_script = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a nav_menu file at the top of the
    # 'shared_models/shared_entry_form.html' template
    nav_menu = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a site_css file at the top of the
    # 'shared_models/shared_entry_form.html' template
    site_css = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a field_list in the context var

    # this is a list of fields used for describing the context variable called 'object'
    field_list = None

    # This is a subtitle that will be appended to the title of the webpage tab in the browser. e.g., Title - subtitle
    subtitle = None

    # title h1
    h1 = None
    # title h2
    h2 = None
    # title h3
    h3 = None

    # stuff for breadcrumbs
    #########################
    # should be a simple string
    active_page_name_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    parent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    grandparent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    greatgrandparent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    root_crumb = None
    # this can be used in the case of simple breadcrumbs where we are just going from index > active page; this will override anything provided in the root_crumb var
    home_url_name = None
    # should the yes/no fields be colored?
    color_boolean = True
    # container class to user
    container_class = "container"

    # should import vueJS 2?
    import_vue_2 = None

    # should import vueJS 2?
    import_vue_3 = None

    # should import leaflet 2?
    import_leaflet = None

    def get_import_vue_2(self):
        return self.import_vue_2

    def get_import_vue_3(self):
        return self.import_vue_2

    def get_import_leaflet(self):
        return self.import_leaflet

    def get_color_boolean(self):
        return self.color_boolean

    def get_title(self):
        return self.title

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_java_script(self):
        return self.java_script

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_nav_menu(self):
        return self.nav_menu

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_site_css(self):
        return self.site_css

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_field_list(self):
        return self.field_list

    def get_subtitle(self):
        return self.subtitle

    def get_h1(self):
        return self.h1

    def get_h2(self):
        return self.h2

    def get_h3(self):
        return self.h3

    def get_active_page_name_crumb(self):
        return self.active_page_name_crumb

    def get_parent_crumb(self):
        return self.parent_crumb

    def get_grandparent_crumb(self):
        return self.grandparent_crumb

    def get_greatgrandparent_crumb(self):
        return self.greatgrandparent_crumb

    def get_root_crumb(self):
        return self.root_crumb

    def get_crumbs(self):
        """
        Certain templates expect a context variable called crumbs the structure of this var is a list of dicts.
        Each dict has a title and url except the active crumb which only needs a title'''
        """

        root = self.get_root_crumb()
        greatgrandparent = self.get_greatgrandparent_crumb()
        grandparent = self.get_grandparent_crumb()
        parent = self.get_parent_crumb()
        active_page_name = self.get_active_page_name_crumb()

        # if there is not an active page, we will take either the h1 or title or subtitle if available
        if not active_page_name:
            if self.get_h1():
                active_page_name = self.get_h1()
            elif self.get_title():
                active_page_name = self.get_title()
            elif self.get_subtitle():
                active_page_name = self.get_subtitle()

        # if there is still no active page name, we are out of business: no crumbs
        if active_page_name:
            crumbs = list()

            # first see if there is a home_url_name
            if self.home_url_name:
                crumbs.append({"title": _("Home"), "url": reverse(self.home_url_name)})

            elif root:
                crumbs.append(root)

            if greatgrandparent:
                crumbs.append(greatgrandparent)

            if grandparent:
                crumbs.append(grandparent)

            if parent:
                crumbs.append(parent)

            crumbs.append({"title": active_page_name})
            return crumbs

    def get_container_class(self):
        return self.container_class

    def get_query_string(self):
        if self.request.META['QUERY_STRING'] and self.request.META['QUERY_STRING'] != "":
            return "?" + self.request.META['QUERY_STRING']
        return ""

    def get_common_context(self) -> dict:
        context = dict()

        title = self.get_title()
        h1 = self.get_h1()

        if title:
            context['title'] = title

        if h1:
            context['h1'] = h1

        java_script = self.get_java_script()
        nav_menu = self.get_nav_menu()
        site_css = self.get_site_css()

        field_list = self.get_field_list()
        h2 = self.get_h2()
        h3 = self.get_h3()
        subtitle = self.get_subtitle()
        crumbs = self.get_crumbs()
        container_class = self.get_container_class()

        if java_script:
            context['java_script'] = java_script

        if nav_menu:
            context['nav_menu'] = nav_menu

        if site_css:
            context['site_css'] = site_css

        if field_list:
            context['field_list'] = field_list

        if subtitle:
            context['subtitle'] = subtitle
        # if there is no subtitle, use the h1 as a default
        elif self.get_crumbs():
            context['subtitle'] = self.get_crumbs()[-1].get("title")
        elif h1:
            context['subtitle'] = h1
        elif title:
            context['subtitle'] = title

        if h1:
            context['h1'] = h1

        if h2:
            context['h2'] = h2

        if h3:
            context['h3'] = h3

        if crumbs:
            context['crumbs'] = crumbs

        context['container_class'] = container_class
        context["color_boolean"] = self.get_color_boolean()
        context["import_vue_2"] = self.get_import_vue_2()
        context["import_vue_3"] = self.get_import_vue_3()
        context["import_leaflet"] = self.get_import_leaflet()

        return context


class CommonFormMixin(CommonMixin):
    cancel_url = None
    cancel_text = _("Back")
    submit_text = _("Submit")
    submit_btn_class = "btn-warning"
    cancel_btn_class = "btn-secondary"
    editable = True
    is_multipart_form_data = False

    def get_is_multipart_form_data(self):
        return self.is_multipart_form_data

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        elif self.get_parent_crumb():
            return self.get_parent_crumb().get("url")
        elif self.home_url_name:
            return reverse(self.home_url_name)
        else:
            return self.request.META.get('HTTP_REFERER')

    def get_cancel_text(self):
        return self.cancel_text

    def get_submit_text(self):
        return self.submit_text

    def get_editable(self):
        return self.editable

    def get_submit_btn_class(self):
        return self.submit_btn_class

    def get_cancel_btn_class(self):
        return self.cancel_btn_class

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        # if there is no success url provided, a reasonable guess would be to go back to the parent url
        elif self.get_parent_crumb():
            return self.get_parent_crumb().get("url")

    def get_common_context(self):
        context = super().get_common_context()
        context['cancel_url'] = self.get_cancel_url()
        context['cancel_text'] = self.get_cancel_text()
        context['submit_text'] = self.get_submit_text()
        context['editable'] = self.get_editable()
        context["submit_btn_class"] = self.get_submit_btn_class()
        context["cancel_btn_class"] = self.get_cancel_btn_class()
        context["is_multipart_form_data"] = self.get_is_multipart_form_data()

        return context

class OpenAIView(CommonFormMixin, CreateView):
    template_name = 'openai.html'

    def post(self, request, *args, **kwargs):
        # Extract files from the request.
        csv_file = request.FILES.get('csv_file')
        pdf_file = request.FILES.get('pdf_file')

        # Validate that both files are present.
        if not csv_file or not pdf_file:
            # Return an error response if either file is missing.
            return JsonResponse({'error': "Both a CSV and a PDF file are required."}, status=400)

        # Save the uploaded files to media storage and get their paths.
        csv_file_path = self.save_file(csv_file, 'csv')
        pdf_file_path = self.save_file(pdf_file, 'pdf')

        # Initialize document processing classes with the uploaded files. CA is for combined files
        document_type = model.DocumentType("CA", csv_file_path)
        document = model.Document(pdf_file, document_type)

        # Determine the output CSV file name based on the PDF file name.
        base_pdf_file_name = document.get_file_name(pdf_file.name)
        csv_file_name = f"{os.path.splitext(base_pdf_file_name)[0]}.csv"

        try:
            # Attempt to get responses from OpenAI for the document content.
            openai_responses = document.get_openai_responses()
        except Exception as e:
            # Log and return an error if something goes wrong during processing.
            print(f"Error while getting responses from OpenAI: {e}")
            return JsonResponse({'error': "An error occurred while processing your request. Please try again."}, status=500)

        # Prepare for writing the CSV output.
        csv_output = io.StringIO()
        writer = csv.writer(csv_output)

        # Write the headers (keys from the OpenAI responses) to the CSV.
        headers = list(openai_responses.keys())
        writer.writerow(headers)

        # Initialize lists to store the main response and source information.
        responses = []
        sources = []

        # Split the OpenAI response into the main response and source, then store them.
        for header in headers:
            parts = openai_responses[header].split('Source:', 1)  
            responses.append(parts[0].strip())  # Main response text.
            sources.append(parts[1].strip() if len(parts) > 1 else "N/A")  # Source text, or "N/A" if not present.

        # Write the main responses and sources to the next two rows in the CSV.
        writer.writerow(responses)
        writer.writerow(sources)

        # Get the CSV data as a string and close the StringIO object.
        csv_data = csv_output.getvalue()
        csv_output.close()

        return JsonResponse({'csv_content': csv_data, 'filename': csv_file_name})


    def save_file(self, file, file_type):
        """
        Saves an uploaded file to the media directory and returns the path to the saved file.
        """
        file_name = default_storage.save(f'documents/{file.name}', ContentFile(file.read()))
        file_path = default_storage.path(file_name)
        return file_path

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'h1': self.h1,
        })
    '''
    Read the content of a text document located at the specified path and return it as a string.
    Parameters:
      - path (str): File path to the text document that needs to be read.
    Return Value:
      - doc_content (str): Content of the file as a string
    '''
    def get_content(self, path):
        content = ""
        reader = PdfReader(path)
        for page in reader.pages:
            content += page.extract_text()
        return content
    
    """
    turns list of dicts into a pd dataframe

    dict_list: List, list of openai responces
    Return: pandas DataFrame, proccessed data for output
    """
    def convert_dict_to_db(self, res_list):
        output = pd.DataFrame()
        dictionary_df = pd.DataFrame(res_list)
        output = pd.concat([output, dictionary_df], ignore_index=True)
        return output

    """
    turns dataframe into csv file

    output_df: DataFrame, created using pandas
    Return: Null, creates .csv file in data folder
    """
    def convert_to_csv(self, output_df):
        output_df.to_csv('output/three_full_sample.csv', index=False)