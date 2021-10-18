from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q,Exists
import base64
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes,force_str

# Create your models here.

class Customer(models.Model):
    PLANS = (('Diamond','Diamond'),('Gold','Gold'),('Silver','Silver'))
    user = models.OneToOneField(User,null = True,on_delete = models.CASCADE,default=True)
    name  = models.CharField(null=True,max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)

    created = models.DateTimeField(null=True,auto_now=False,auto_now_add=True)
    plans = models.CharField(max_length=200,choices=PLANS,default= 'PLANS[0]')
    profile_pic = models.ImageField(default="images/propic.jpeg/",null=True,blank=True)
    url_link = models.CharField(null=True,max_length=350)

    def __str__(self):
        return str(self.user)

    def create_url_link(self):
        signup_link = 'accounts/signup'
        name = self.user.username
        link = f'http://127.0.0.1:8000/{signup_link}/{name}/'
        print(link)
        return link

    def get_absolute_url(self):
        return reverse('customer',kwargs={"uidb64": self.get_decode()})



class Container(models.Model):
    name = models.CharField(null=True, max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)

    def create_cust_container_url(self):
        return reverse('create_cust_container', kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse('container',kwargs={'id':self.name})

class customer_container(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    container = models.ForeignKey(Container,on_delete=models.CASCADE,null=True)
    tracking_number =  models.CharField(null=True, max_length=200)
    longitude = models.IntegerField(null=True)
    latitude = models.IntegerField( null=True)

    def __str__(self):

        return str(self.user.username + self.container.name + str(self.pk))

    def create_tracking_id(self):
        idd = str(self.pk)
        name = self.user.username
        ini_token = f"{idd}{name}{self.container.name}"
        token = (base64.b64encode(force_bytes(ini_token)))
        print(token)
        #print(base64.b64decode(force_str(token)))
        #print(str(base64.b64encode(force_bytes(ini_token))))
        return token

class reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(null=True, max_length=200)
    message = models.TextField(null=True)

class container_item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    container = models.ForeignKey(customer_container,on_delete=models.CASCADE,null=True)
    name = models.CharField(null=True,max_length=200)
    description = models.TextField(null=True)
    tracking_number = models.CharField(null=True, max_length=200)
    longitude = models.IntegerField( null=True)
    latitude = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.container}{self.name}"

    def create_tracking_id(self):
        idd = str(self.pk)
        name = self.user.username
        ini_token = f"{idd}{name}{self.container.name}"
        token = (base64.b64encode(force_bytes(ini_token)))
        print(token)
        #print(base64.b64decode(force_str(token)))
        #print(str(base64.b64encode(force_bytes(ini_token))))
        return token
