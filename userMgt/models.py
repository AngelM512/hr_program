import email
from django.db import models
from django.contrib.auth.models import User
from PIL import Image




class Company(models.Model):
    name    = models.CharField(blank=True, max_length=45)
    address = models.CharField(blank=True, max_length=255)
    def __str__(self):
        return self.name



class Employee(models.Model):
    first_name    = models.CharField(max_length=20,blank=False)
    last_name     = models.CharField(max_length=20,blank=False)
    prefered_name = models.CharField(max_length=20,blank=True)
    birth_date    = models.DateField()
    gender        = models.CharField(max_length=1)
    salary        = models.IntegerField()
    hired_date    = models.DateField()
    department    = models.CharField(max_length=45)
    email         = models.EmailField(max_length=254, blank=True)

    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                )

    def __str__(self) -> str:
        return (self.first_name +' '+ self.last_name)



class Profile(models.Model): #company's profile model
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    company = models.OneToOneField(
                Company, 
                on_delete=models.CASCADE,
                null=True,
                blank=True,
            )

    def __str__(self):

        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path) #get the user's image

        # check and rezise before opening
        if img.height >= 300 or img.width >= 300:

            output_size = (300, 300)

            img.thumbnail(output_size)

            img.save(self.image.path,)
    



