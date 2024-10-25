from django import forms
from django.forms import DateInput
from .models import User, Staffs, Librarian, Students,Books, Libraryrecord, Fees

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = ['address']  # Include other fields you want to show


class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']  # Add other fields as needed

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.user_type = '2'  # Ensure the user type is set to Staff
        if commit:
            user.save()
        return user
    

class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['address']  # Add other librarian-specific fields here


class UserlForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']  # User fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.user_type = '3'  # Set the user_type to Librarian
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['firstname', 'lastname', 'dob', 'email', 'gender', 'address', 'course','session_start_year', 'session_end_year']
        widgets = {
            'session_start_year': forms.SelectDateWidget(),  # Optional: to show a date picker
            'session_end_year': forms.SelectDateWidget(),
        }
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author', 'count_books']


class LibraryRecordForm(forms.ModelForm):
    class Meta:
        model = Libraryrecord
        fields = ['student', 'book', 'borrowed_date']  # Include borrowed_date in fields
        widgets = {
            'borrowed_date': DateInput(),  # Date input widget
        }

    student = forms.ModelChoiceField(queryset=Students.objects.all(), label="Select Student")
    book = forms.ModelChoiceField(queryset=Books.objects.all(), label="Select Book")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default value of borrowed_date to today's date
        self.fields['borrowed_date']

       
STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Paid'),
    ]

class FeesForm(forms.ModelForm):
    
    class Meta:
        model = Fees
        fields = ['student', 'amount', 'status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES)
        }