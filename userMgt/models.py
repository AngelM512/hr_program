import email
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model): #company's profile model
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    

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
    
# def Company_member():

#
#
#
#
class Company(models.Model):
    name    = models.CharField(blank=True, max_length=45)
    address = models.CharField(blank=True, max_length=255)
    
    #UPDATE: profile now 
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True, 
                                    )
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




#Update: introduce a company membership model that 
#associates User and its correcding id to many companys id
#and give it a role as ADMIN, SUPERVISOR/MANAGER OF COMPANY, W2_EMPLOYEE
class Company_Membership(models.Model):


    #get user,company,role and make a relationship
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    
    company = models.ForeignKey(Company,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   )
    role = models.CharField(max_length=20, blank=False)


    #assign roles  as ADMIN, SUPERVISOR/MANAGER OF COMPANY, W2_EMPLOYEE
    class Assing_Role(models.TextChoices):
        ADMIN = '1','admin' #NO PERMISSIONS IT IS GOD
        
        MANAGEMENT = '2','management' #SUPERVISOR/MANAGER/CEO WILL HAVE LIMITED PERMISSIONS WITHIN THE COMPANY

        EMPLOYEE ='3','employee' #W2 REGULAR
  
    #configurations of Company_Membership
    class Meta:

       #constraints: same user_id can exist/work in different 
       # companys but there can be two user_id with same id 
       # working in the same company. 
        constraints = [
            
            models.UniqueConstraint(
                fields=['user','company'],
                name='unique_user_to_company_relation', )
            ]

    choices = models.CharField(max_length=2,
                choices=Assing_Role.choices,
                default=Assing_Role.EMPLOYEE)
                
        #assign roles  as ADMIN, SUPERVISOR/MANAGER OF COMPANY, W2_EMPLOYEE




            
