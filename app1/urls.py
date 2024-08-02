from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='Home'),
    path('add',views.add_records, name="Add Document"),

    path('delete',views.delete_records, name="Delete"),
    path('update/', views.list_documents, name='list_documents'),
    path('edit/<str:doc_id>/', views.edit_document, name='edit_document'),
]