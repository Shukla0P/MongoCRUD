from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='Home'),
    path('add',views.add_records, name="Add Document"),

    path('delete/', views.delete_document, name='delete_document'),
    path('confirm_delete/<str:database_name>/<str:collection_name>/<str:doc_id>/', views.confirm_delete, name='confirm_delete'),
    path('update/', views.list_documents, name='list_documents'),
    path('edit/<str:database_name>/<str:collection_name>/<str:doc_id>/', views.edit_document, name='edit_document'),
]