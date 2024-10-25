from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Staff"),(3,"Librarian"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin.username 


class Librarian(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.admin.username 


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    dob=models.DateField()
    email=models.EmailField()
    gender=models.CharField(max_length=255)
    address=models.TextField()
    course=models.CharField(max_length=255)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class Fees(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)  # True if paid, False if unpaid
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - {self.amount} - {'Pending' if self.status else 'paid'}"


class Books(models.Model):
    id= models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    count_books= models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 


class Libraryrecord(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    book = models.ForeignKey('Books', on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(default=timezone.now)
    returned_date = models.DateTimeField(null=True, blank=True)  # Allow nulls until the book is returned
    status = models.IntegerField(default=0)  # 0 for not returned, 1 for returned

    def return_date_time():
        return timezone.now() + timezone.timedelta(days=7)
    

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type==2:
            Librarian.objects.create(admin=instance,address="")

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.librarian.save()
    