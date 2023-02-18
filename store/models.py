from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator,MaxValueValidator



# Create your models here.




class Category(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Products(models.Model):
    product_name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    price=models.PositiveBigIntegerField()
    is_active=models.BooleanField(default=True)
    image=models.ImageField()

    def __str__(self):
        return self.product_name

    @property
    def offer_price(self):
        offs=Offers.objects.filter(product=self)

        if offs:
            off=offs[0]
            offer_price=self.price - off.discount
            return offer_price
        else:
            return self.price
            
    @property
    def p_reviews(self):
        qs=Reviews.objects.filter(product=self)
        return qs

    @property
    def avg_rating(self):
        qs=self.p_reviews
        if qs:
            total=sum([r.rating for r in qs])
            return total/len(qs)
        else:
            return 0

        


class Carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("in-cart","in-cart"),
        ("order_placed","order_placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")
    qty=models.PositiveIntegerField(default=1)


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("shipped","shipped"),
        ("order-placed","oreder_placed"),
        ("in-transist","in-transist"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
        ("return","return")
    )
    status=models.CharField(max_length=200,choices=options,default="oreder-placed")
    curdate=datetime.date.today()
    expdate=curdate+datetime.timedelta(days=5)
    expected_deliverydate=models.DateField(default=expdate)
    address=models.CharField(max_length=200,null=True)


class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    comment=models.CharField(max_length=240)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.comment



class Offers(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    discount=models.PositiveIntegerField(default=0)
    isAvailable=models.BooleanField(default=True)
    start_date=models.DateField(default=datetime.date.today)
    end_date=models.DateField(default=datetime.date.today)





