from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient
from .forms import AddDocumentForm, DocumentSelectionForm, EditDocumentForm
import json
from bson import ObjectId
from django.views.decorators.http import require_POST

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
            
            try:
                # Replace with your MongoDB URI
                client = MongoClient("mongodb://localhost:27017/")
                db = client[database_name]
                collection = db[collection_name]
                
                # Insert the document into the collection
                result = collection.insert_one(document)
                
                return JsonResponse({'status': 'success', 'inserted_id': str(result.inserted_id)})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
    
    else:
        form = AddDocumentForm()
    
    return render(request, 'add_document.html', {'form': form})
                  
def list_documents(request):
    formatted_documents = []
    form = DocumentSelectionForm(request.POST)

    if request.method == "POST" and form.is_valid():
        database_name = form.cleaned_data['database_name']
        collection_name = form.cleaned_data['collection_name']

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
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
                'doc_id': str(doc_id),  # Convert ObjectId to string for URL usage
                'database_name': database_name,
                'collection_name': collection_name
            })

    context = {
        'form': form,
        'formatted_documents': formatted_documents,
    }
    return render(request, 'list_documents.html', context)

def edit_document(request, database_name, collection_name, doc_id):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client[database_name]
    collection = db[collection_name]

    if request.method == 'POST':
        form = EditDocumentForm(request.POST)
        if form.is_valid():
            document_data = form.cleaned_data['document_data']
            # Convert the document data from JSON string to dictionary
            updated_document = json.loads(document_data)
            del updated_document['_id']

            try:
                # Update the document in the collection
                result = collection.update_one({'_id': ObjectId(doc_id)}, {'$set': updated_document})

                return JsonResponse({'status': 'success', 'matched_count': result.matched_count, 'modified_count': result.modified_count})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            # If the form is not valid, print the form errors
            print("Form is not valid")
            print(form.errors)
    
    else:
        # Convert doc_id to ObjectId
        try:
            object_id = ObjectId(doc_id)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid document ID: {e}'})

        # Fetch the document from the database
        document = collection.find_one({'_id': object_id})
        print(document)

        if not document:
            return JsonResponse({'status': 'error', 'message': 'Document not found'})

        document['_id'] = str(document['_id'])
                         
        # Pre-fill the form with the document data
        form = EditDocumentForm(initial={
            'document_id': str(document['_id']),
            'document_data': json.dumps(document, indent=4)
        })

    return render(request, 'edit_document.html', {'form': form, 'database_name': database_name, 'collection_name': collection_name, 'doc_id': doc_id})

@require_POST
def delete_document(request):
    database_name = request.POST.get('database_name')
    collection_name = request.POST.get('collection_name')
    document_id = request.POST.get('document_id')

    try:
        # Replace with your MongoDB URI
        client = MongoClient("mongodb://localhost:27017/")
        db = client[database_name]
        collection = db[collection_name]

        # Convert document_id to ObjectId
        object_id = ObjectId(document_id)

        # Delete the document from the collection
        result = collection.delete_one({'_id': object_id})

        if result.deleted_count == 0:
            return JsonResponse({'status': 'error', 'message': 'Document not found'})
        
        return redirect('list_documents')  # Redirect to the list documents page
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def confirm_delete(request, database_name, collection_name, doc_id):
    try:
        # Replace with your MongoDB URI
        client = MongoClient("mongodb://localhost:27017/")
        db = client[database_name]
        collection = db[collection_name]

        # Convert document_id to ObjectId
        object_id = ObjectId(doc_id)

        # Find the document to confirm deletion
        document = collection.find_one({'_id': object_id})

        if not document:
            return HttpResponse("Document not found", status=404)

        # Convert ObjectId to string in the document
        document['_id'] = str(document['_id'])

        context = {
            'document': document,
            'database_name': database_name,
            'collection_name': collection_name,
            'doc_id': doc_id,
        }
        return render(request, 'confirm_delete.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
def home(request):
    db_names=client.list_database_names()
    return render(request, 'home.html',{'databases':db_names})
