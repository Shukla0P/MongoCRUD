from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from .forms import AddDocumentForm, DocumentSelectionForm, EditDocumentForm
import json

client = MongoClient("localhost", 27017)

def add_records(request):
    if request.method == 'POST':
        form = AddDocumentForm(request.POST)
        if form.is_valid():
            database_name = form.cleaned_data['database_name']
            collection_name = form.cleaned_data['collection_name']
            document_data = form.cleaned_data['document_data']
            
            # Convert the document data from JSON string to dictionary
            document = json.loads(document_data)
            
            # Replace with your MongoDB URI
            client = MongoClient("mongodb://localhost:27017/")
            db = client[database_name]
            collection = db[collection_name]
            
            # Insert the document into the collection
            result = collection.insert_one(document)
                  
def list_documents(request):
    formatted_documents = []
    form = DocumentSelectionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        database_name = form.cleaned_data['database_name']
        collection_name = form.cleaned_data['collection_name']

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')  # Adjust connection string if needed
        db = client[database_name]
        collection = db[collection_name]

        # Fetch all documents from the specified collection
        documents = list(collection.find())
        
        # Convert each document to a formatted string
        for doc in documents:
            doc_id = doc.get('_id')
            formatted_str = '\n'.join(f"{key}: {value}" for key, value in doc.items() if key != '_id')
            formatted_documents.append({
                'formatted_str': formatted_str,
                'doc_id': str(doc_id)  # Convert ObjectId to string for URL usage
            })

    context = {
        'form': form,
        'formatted_documents': formatted_documents,
    }
    return render(request, 'list_documents.html', context)

def edit_document(request, doc_id):
    client = MongoClient('mongodb://localhost:27017/')  # Adjust connection string if needed

    database_name = str(request.GET.get('database_name'))
    collection_name = str(request.GET.get('collection_name'))

    db = client[database_name]
    collection = db[collection_name]
    
    if request.method == "POST":
        form = EditDocumentForm(request.POST)
        if form.is_valid():
            update_data = form.cleaned_data['document_data']
            # Update the document
            collection.update_one({'_id': doc_id}, {'$set': update_data})
            print("inside POST")
            return redirect('list_documents')
    else:
        document = collection.find_one({'_id': doc_id})
        # Initialize form with document data
        form = EditDocumentForm(initial={
            'database_name': database_name,
            'collection_name': collection_name,
            'document_data': document
        })

    # Ensure 'document' is always defined before rendering
    document = collection.find_one({'_id': doc_id})

    return render(request, 'edit_document.html', {'form': form, 'document': document})

def update_records(request):
    return HttpResponse("Here we'll update existing record")

def delete_records(request):
    return HttpResponse("This page is for deleting the records")

def home(request):
    db_names=client.list_database_names()
    return render(request, 'home.html',{'databases':db_names})
