from django import forms
from django.forms import DateInput
from .models import User, Staffs, Librarian, Students,Books, Libraryrecord, Fees

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = ['address']  


class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password'] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  
        user.user_type = '2' 
        if commit:
            user.save()
        return user
    

class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['address'] 


class UserlForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        user.user_type = '3'  
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['firstname', 'lastname', 'dob', 'email', 'gender', 'address', 'course','session_start_year', 'session_end_year']
        widgets = {
            'session_start_year': forms.SelectDateWidget(), 
            'session_end_year': forms.SelectDateWidget(),
        }
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title','author', 'count_books']


class LibraryRecordForm(forms.ModelForm):
    class Meta:
        model = Libraryrecord
        fields = ['student', 'book', 'borrowed_date']  
        widgets = {
            'borrowed_date': DateInput(),  
        }

    student = forms.ModelChoiceField(queryset=Students.objects.all(), label="Select Student")
    book = forms.ModelChoiceField(queryset=Books.objects.all(), label="Select Book")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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