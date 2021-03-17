from django.db import models
from django.urls import reverse
# Create your models here.


class Customer(models.Model):

    GENDER_LIST = (
        ('Male','Male'),
        ('Female', 'Female'),
    )

    email = models.EmailField(max_length=100, unique=True, null=True)
    f_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER_LIST, default=GENDER_LIST[0][0])
    is_valid = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f'{self.l_name} {self.f_name} {self.m_name}'

class CustomerTable(models.Model):

    STATUS_LIST = (
        ('Occupied','Occupied'),
        ('Unoccupied', 'Unoccupied'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250) 
    capacity = models.IntegerField()
    status = models.CharField(max_length=250, choices=STATUS_LIST, default=STATUS_LIST[1][0])  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ropms:menu_selection', args=[self.id])

class Menu(models.Model):

    CATEGORY_LIST = (
        ('Beverages', 'Beverages'),
        ('Break Fast', 'Break Fast'),
        ('Desserts', 'Desserts'),
        ('Vegetables', 'Vegetables'),
        ('Soup', 'Soup'),
        ('Salad', 'Salad'),
        ('Main Course', 'Main Course'),
    )

    STATUS_LIST = (
        ('Available','Available'),
        ('Unavailable', 'Unavailable'),
    )
    
    image = models.FileField(upload_to="images/")
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_LIST, default=STATUS_LIST[0][0])
    category = models.CharField(max_length=50, choices=CATEGORY_LIST, default=CATEGORY_LIST[0][0])
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("ropms:menu_detail", args=[self.id])

class Waiting(models.Model):
    customer = models.OneToOneField(Customer, related_name="customer", on_delete=models.CASCADE)
    table = models.OneToOneField(CustomerTable, related_name="table", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.customer)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name="cart_fk_customer", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, related_name="cart_fk_menu_item", on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    date_added = models.DateTimeField(auto_now_add=True) 
 
    def __str__(self):
        return str(self.menu_item)