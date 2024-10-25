from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .models import Students, Fees, Libraryrecord, User, Staffs, Librarian, Books
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import FormView, View, ListView,CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import StaffForm, UsersForm, LibrarianForm, UserlForm, StudentForm,BookForm, LibraryRecordForm, FeesForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from datetime import timedelta
from django.db.models import Q



def index(request):
    return render(request, 'admin/index.html')

def admindashboard(request):
    return render(request, 'admin/dashborad.html')

def staffdashboard(request):
    return render(request, 'staff/staff_dashboard.html')

def librariandashboard(request):
    return render(request, 'library/librarian_dashboard.html')

def errorpage(request):
    return render(request, 'shared/error.html')

class CustomLoginView(FormView):
    template_name = 'admin/login.html' 
    form_class = AuthenticationForm  
    success_url = '/'  
    def form_valid(self, form):
       
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

            # Check user type and redirect accordingly
            if user.user_type == '1':
                return redirect('admin_dashboard')  # Admin dashboard URL
            elif user.user_type == '2':
                return redirect('staff_dashboard')  # Staff dashboard URL
            elif user.user_type == '3':
                return redirect('librarian_dashboard')  # Librarian dashboard URL

        # If authentication fails
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)  
    
def logout_view(request):
    logout(request)
    return redirect('login')


class AddStaffView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.user_type == '1'  # Only allow admins to access this view

    def get(self, request):
        user_form = UsersForm()
        staff_form = StaffForm()
        return render(request, 'admin/add_staff.html', {'user_form': user_form, 'staff_form': staff_form})

    def post(self, request):
        user_form = UsersForm(request.POST)
        staff_form = StaffForm(request.POST)
        
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            staff = staff_form.save(commit=False)
            staff.admin = user  
            staff.save()
            return redirect('staff_list')  # Redirect after successful creation

        return render(request, 'admin/add_staff.html', {'user_form': user_form, 'staff_form': staff_form})
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    
    
class StaffListView(UserPassesTestMixin, ListView):
    model = Staffs
    template_name = 'admin/staff_list.html'
    context_object_name = 'staffs'

    def test_func(self):
        return self.request.user.user_type == '1' 
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class EditStaffView(UserPassesTestMixin, View):
    # Role-based access control
    def test_func(self):
        return self.request.user.user_type == '1'  # Only admins can access

    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access

    def get(self, request, staff_id):
        staff_member = get_object_or_404(Staffs, id=staff_id)  
        user_form = UsersForm(instance=staff_member.admin)  
        staff_form = StaffForm(instance=staff_member)  
        
        return render(request, 'admin/edit_staff.html', {
            'user_form': user_form,
            'staff_form': staff_form,
            'staff_member': staff_member
        })

    def post(self, request, staff_id):
        staff_member = get_object_or_404(Staffs, id=staff_id) 
        user_form = UsersForm(request.POST, instance=staff_member.admin) 
        staff_form = StaffForm(request.POST, instance=staff_member) 
        
        if user_form.is_valid() and staff_form.is_valid():
            user_form.save()  
            staff_form.save()  
            
            return redirect('staff_list')  

        return render(request, 'admin/edit_staff.html', {
            'user_form': user_form,
            'staff_form': staff_form,
            'staff_member': staff_member
        })
    

class DeleteStaffView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.user_type == '1'  # Only admins can delete staff

    def post(self, request, staff_id):
        staff_member = get_object_or_404(Staffs, id=staff_id)
        staff_member.admin.delete() 
        staff_member.delete()
        return redirect('staff_list')  

    
    

class AddLibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin users can access this view

    def get(self, request):
        user_form = UserlForm()
        librarian_form = LibrarianForm()
        return render(request, 'admin/add_librarian.html', {'user_form': user_form, 'librarian_form': librarian_form})

    def post(self, request):
        user_form = UserlForm(request.POST)
        librarian_form = LibrarianForm(request.POST)
        
        if user_form.is_valid() and librarian_form.is_valid():
            user = user_form.save()  
            librarian = librarian_form.save(commit=False)
            librarian.admin = user  
            librarian.save()
            return redirect('librarian_list') 

        return render(request, 'admin/add_librarian.html', {'user_form': user_form, 'librarian_form': librarian_form})
    
    def handle_no_permission(self):
        return redirect('error')  
    

class LibrarianListView(UserPassesTestMixin, ListView):
    model = Librarian
    template_name = 'admin/librarian_list.html'
    context_object_name = 'librarians'

    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin users can view the librarian list
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class EditLibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin users can access this view

    def get(self, request, pk):
        librarian = Librarian.objects.get(pk=pk)
        user_form = UserlForm(instance=librarian.admin)
        librarian_form = LibrarianForm(instance=librarian)
        return render(request, 'admin/edit_librarian.html', {'user_form': user_form, 'librarian_form': librarian_form})

    def post(self, request, pk):
        librarian = Librarian.objects.get(pk=pk)
        user_form = UserlForm(request.POST, instance=librarian.admin)
        librarian_form = LibrarianForm(request.POST, instance=librarian)

        if user_form.is_valid() and librarian_form.is_valid():
            user_form.save()
            librarian_form.save()
            return redirect('librarian_list')

        return render(request, 'admin/edit_librarian.html', {'user_form': user_form, 'librarian_form': librarian_form})


class DeleteLibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin users can access this view

    def post(self, request, pk):
        librarian = Librarian.objects.get(pk=pk)
        librarian.admin.delete() 
        librarian.delete()
        return redirect('librarian_list')

    
    
# student
class AddStudentView(UserPassesTestMixin, CreateView):
    model = Students
    form_class = StudentForm
    template_name = 'admin/add_student.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin can access
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class EditStudentView(UserPassesTestMixin, UpdateView):
    model = Students
    form_class = StudentForm
    template_name = 'admin/edit_student.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin can access
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class DeleteStudentView(UserPassesTestMixin, View):
    def post(self, request, student_id):
        student = get_object_or_404(Students, id=student_id)
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return JsonResponse({'success': True, 'message': 'Student deleted successfully!'})

    def test_func(self):
        return self.request.user.user_type == '1'  # Only Admin can access

    def handle_no_permission(self):
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    

class StudentListView(UserPassesTestMixin, ListView):
    model = Students
    template_name = 'admin/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def test_func(self):
        return self.request.user.user_type in ['1', '2', '3']  # Admin, Staff, Librarian

    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

#Library

class AddBookView(UserPassesTestMixin, CreateView):
    model = Books
    form_class = BookForm
    template_name = 'library/add_book.html'
    success_url = reverse_lazy('book_list')  

    def test_func(self):
        return self.request.user.user_type in ['1', '3']  # 1: Admin, 3: Librarian
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class BookListView(UserPassesTestMixin, ListView):
    model = Books
    template_name = 'library/book_list.html'  
    context_object_name = 'books'  
    paginate_by = 10  

    # Allow only admins and librarians to view the book list
    def test_func(self):
        return self.request.user.user_type in ['1', '3']  # 1: Admin, 3: Librarian
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access


class EditBookView(UserPassesTestMixin, UpdateView):
    model = Books
    form_class = BookForm
    template_name = 'library/edit_book.html'
    success_url = reverse_lazy('book_list')  

    # Allow only admins and librarians to edit books
    def test_func(self):
        return self.request.user.user_type in ['1', '3']
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access

    

class AddLibraryRecordView(UserPassesTestMixin, CreateView):
    model = Libraryrecord
    form_class = LibraryRecordForm
    template_name = 'library/add_library_record.html'
    success_url = reverse_lazy('library_record_list') 

    # Allow only admins and librarians to add library records
    def test_func(self):
        return self.request.user.user_type in ['1', '3']  # 1: Admin, 3: Librarian
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access

    # Handle form submission
    def form_valid(self, form):
        library_record = form.save(commit=False)  
        book = library_record.book  

        # Check if the book has available copies
        if book.count_books > 0:
            book.count_books -= 1  # Decrease the available book count
            book.save()  

            # Save the library record with borrow details
            library_record.borrowed_date = timezone.now()  # Set the borrowed date to the current time
            library_record.returned_date = library_record.borrowed_date + timedelta(days=7)
            library_record.save() 

            return redirect(self.success_url) 
        else:
           
            form.add_error(None, 'No copies of the book are available for borrowing.')
            return self.form_invalid(form)


class LibraryRecordListView(UserPassesTestMixin, ListView):
    model = Libraryrecord
    template_name = 'library/library_record_list.html'
    context_object_name = 'library_records'
    
    # Allow only admins, librarians (user_type 1, 3) to view the library records
    def test_func(self):
        return self.request.user.user_type in ['1','2', '3']

    def handle_no_permission(self):
        return redirect('error')
    
    
class EditLibraryRecordView(UserPassesTestMixin, UpdateView):
    model = Libraryrecord
    form_class = LibraryRecordForm
    template_name = 'library/edit_library_record.html'
    success_url = reverse_lazy('library_record_list')

   
    def test_func(self):
        return self.request.user.user_type in ['1', '3']
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class DeleteLibraryRecordView(UserPassesTestMixin, DeleteView):
    model = Libraryrecord
    success_url = reverse_lazy('library_record_list')

    # Role-based access control
    def test_func(self):
        return self.request.user.user_type in ['1', '3'] 

    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access

    def post(self, request, *args, **kwargs):
        library = self.get_object()  
        library.delete()
        messages.success(request, 'Library record deleted successfully!')
        return JsonResponse({'success': True, 'message': 'Record deleted successfully.'})
    
        

class MarkAsReturnedView(UserPassesTestMixin, View):
    
    def test_func(self):
        return self.request.user.user_type in ['1', '3']  # Admin, Librarian

    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access # 1: Admin, 3: Librarian

    def post(self, request, *args, **kwargs):
        record_id = kwargs.get('pk')
        record = get_object_or_404(Libraryrecord, id=record_id)

       
        record.status = 1 
        record.returned_date = timezone.now()
        
       
        book = record.book
        book.count_books += 1  
        book.save()

        record.save() 

        return redirect('library_record_list')
    


class StudentLibraryHistoryView(UserPassesTestMixin, ListView):
    template_name = 'library/library_record_list.html'
    context_object_name = 'library_records' 

    def test_func(self):
        return self.request.user.user_type in ['1', '2', '3'] 

    def get_queryset(self):
        # Get the search parameter
        search_input = self.request.GET.get('search_input') 

        # Initialize the queryset
        queryset = Libraryrecord.objects.none() 

        if search_input:  
            if search_input.isdigit():
                student = get_object_or_404(Students, id=search_input)  
                queryset = Libraryrecord.objects.filter(student=student)  
            else:
                # Search by first or last name
                queryset = Libraryrecord.objects.filter(
                    student__firstname__icontains=search_input
                ) | Libraryrecord.objects.filter(
                    student__lastname__icontains=search_input
                )

        return queryset

    def get_context_data(self, **kwargs):
        # Get context data
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_input', '') 
        return context
    


#fees

class AddFeesView(UserPassesTestMixin, CreateView):
    model = Fees
    form_class = FeesForm
    template_name = 'staff/add_fees.html'
    success_url = reverse_lazy('fees_list')

    def test_func(self):
        return self.request.user.user_type in ['1', '2']   # Only Admin can access
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class UpdateFeesView(UserPassesTestMixin, UpdateView):
    model = Fees
    form_class = FeesForm
    template_name = 'staff/edit_fees.html'
    success_url = reverse_lazy('fees_list')

    def test_func(self):
        return self.request.user.user_type in ['1', '2']   # Only Admin can access
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class DeleteFeesView(UserPassesTestMixin, View):
    def post(self, request, fees_id):
        fees_record = get_object_or_404(Fees, id=fees_id)
        fees_record.delete()
        messages.success(request, 'Fees record deleted successfully!')
        return redirect('fees_list')
    
    def test_func(self):
        return self.request.user.user_type in ['1', '2'] 
    
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class FeesListView(UserPassesTestMixin, ListView):
    model = Fees
    template_name = 'staff/fees_list.html'
    context_object_name = 'fees_records'
    paginate_by = 10

    def test_func(self):
        return self.request.user.user_type in ['1', '2', '3']  # Admin, Staff, Librarian

    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access
    

class StudentFeesHistoryView(UserPassesTestMixin, ListView):
    model = Fees
    template_name = 'staff/fees_list.html'
    context_object_name = 'fees_records'
    
    def get_queryset(self):
        search_input = self.request.GET.get('search_input', '').strip()
        if search_input:
           
            if search_input.isdigit():
                return Fees.objects.filter(
                    Q(student__id=search_input)  # Only filter by ID
                )
            else:
               
                return Fees.objects.filter(
                    Q(student__firstname__icontains=search_input)
                )
        return Fees.objects.none()  
    def test_func(self):
        return self.request.user.user_type in ['1', '2']  
    def handle_no_permission(self):
        return redirect('error')  # Redirect if no access