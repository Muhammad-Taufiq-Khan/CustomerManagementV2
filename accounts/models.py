from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=11, null= True)
    email = models.CharField(max_length=100, null = True)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    
    def __str__(self):
        return self.name



class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=50, null=True)
    catagory = models.CharField(max_length=50, null=True, choices = CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length = 20, null= True)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product= models.ForeignKey(Product, null = True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    status = models.CharField(max_length=50, null=True, choices = STATUS)
    tag = models.ManyToManyField(Tag)
    def __str__(self):
        return "%s %s %s " %(self.customer, self.product, self.status)
