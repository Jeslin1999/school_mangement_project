from django.urls import path
from school import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_dashboard', views.admindashboard, name='admin_dashboard'),
    path('staff_dashboard', views.staffdashboard, name='staff_dashboard'),
    path('librarian_dashboard', views.librariandashboard, name='librarian_dashboard'),
    path('error', views.errorpage, name='error'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-staff/', AddStaffView.as_view(), name='add_staff'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('edit_staff/<int:staff_id>/', EditStaffView.as_view(), name='edit_staff'),
    path('delete_staff/<int:pk>/', DeleteStaffView.as_view(), name='delete_staff'),

    path('add-librarian/', AddLibrarianView.as_view(), name='add_librarian'),
    path('librarian-list/', LibrarianListView.as_view(), name='librarian_list'),
    path('edit_librarian/<int:pk>/', EditLibrarianView.as_view(), name='edit_librarian'),
    path('delete_librarian/<int:pk>/', DeleteLibrarianView.as_view(), name='delete_librarian'),

    path('students/add/', AddStudentView.as_view(), name='add_student'),
    path('students/edit/<int:pk>/', EditStudentView.as_view(), name='edit_student'),
    path('students/delete/<int:student_id>/', DeleteStudentView.as_view(), name='delete_student'),
    path('students/', StudentListView.as_view(), name='student_list'),


    path('add-book/', AddBookView.as_view(), name='add_book'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/edit-book/<int:pk>/', EditBookView.as_view(), name='edit_book'),
    path('historyadd/', AddLibraryRecordView.as_view(), name='add_library_record'),
    path('records/', LibraryRecordListView.as_view(), name='library_record_list'),
    path('records/edit/<int:pk>/', EditLibraryRecordView.as_view(), name='edit_library_record'),
    path('records/delete/<int:pk>/', DeleteLibraryRecordView.as_view(), name='delete_library_record'),
     path('records/return/<int:pk>/', MarkAsReturnedView.as_view(), name='mark_as_returned'),
    path('records/history/', StudentLibraryHistoryView.as_view(), name='student_library_history'),

    path('fees/add/', AddFeesView.as_view(), name='add_fees'),
    path('fees/edit/<int:pk>/', UpdateFeesView.as_view(), name='update_fees'),
    path('fees/delete/<int:fees_id>/', DeleteFeesView.as_view(), name='delete_fees'),
    path('fees/', FeesListView.as_view(), name='fees_list'),
    path('fees/history/', StudentFeesHistoryView.as_view(), name='student_fees_history'),

]