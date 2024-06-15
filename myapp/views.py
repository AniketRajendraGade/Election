from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
from .models import Data
from google.cloud import storage

# def data_create_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('Name')
#         state = request.POST.get('state')
#         district = request.POST.get('District')
#         assembly_constituency = request.POST.get('Assembly_Constituency')
#         files = request.FILES.getlist('file')

#         if state and district and assembly_constituency and files:  # Ensure required fields are filled
#             for file in files:
#                 Data.objects.create(
#                     Name=name,
#                     state=state,
#                     District=district,
#                     Assembly_Constituency=assembly_constituency,
#                     file=file
#                 )
#             return HttpResponse("Succesfully uploaded")  # Replace 'data-list' with your URL name for the list view

#     return render(request, 'index.html')


GS_PROJECT_ID = 'verdant-lattice-425012-f6'
GS_BUCKET_NAME = 'markyticselectiondata'

def data_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        state = request.POST.get('state')
        district = request.POST.get('District')
        assembly_constituency = request.POST.get('Assembly_Constituency')
        files = request.FILES.getlist('file')

        if state and district and assembly_constituency and files:  # Ensure required fields are filled
            for file in files:
                # Save file to Google Cloud Storage
                uploaded_file_url = save_file_to_gcs(file, state, district, assembly_constituency)
                
            return HttpResponse("Successfully uploaded to Google Cloud Storage")

    return render(request, 'index.html')

def save_file_to_gcs(file, state, district, assembly_constituency):
    # Initialize Google Cloud Storage client
    client = storage.Client(project=GS_PROJECT_ID)

    # Get bucket
    bucket = client.bucket(GS_BUCKET_NAME)

    # Define base directory path in the bucket
    base_directory = f"{district}/{assembly_constituency}/"

    # Ensure district and assembly_constituency names are valid for folder creation
    district_folder_name = district
    assembly_folder_name = assembly_constituency

    # Check if the district folder exists in the bucket
    district_blob = bucket.blob(district_folder_name + '/')
    if not district_blob.exists():
        # Create district folder in the bucket
        district_blob.upload_from_string('')

    # Check if the assembly constituency folder exists in the district folder
    assembly_blob = bucket.blob(district_folder_name + '/' + assembly_folder_name + '/')
    if not assembly_blob.exists():
        # Create assembly constituency folder in the district folder
        assembly_blob.upload_from_string('')

    # Create blob object with unique name
    blob = bucket.blob(district_folder_name + '/' + assembly_folder_name + '/' + file.name)

    # Upload file
    blob.upload_from_file(file, content_type=file.content_type)

    # Return public URL of the uploaded file
    return blob.public_url