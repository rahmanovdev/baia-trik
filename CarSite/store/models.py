from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    first_name=models.CharField(max_length=32,null=True,blank=True)
    last_name=models.CharField(max_length=32,null=True,blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(18),
                                                       MaxValueValidator(100)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    data = models.DateField(auto_now_add=True, null=True, blank=True)


class Car(models.Model):
    car_name = models.CharField(max_length=100)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)
    # car_make=models.ForeignKey(CarMake,on_delete=models.CASCADE)
    # model=models.ForeignKey(CarModel,on_delete=models.CASCADE)
    description = models.TextField()
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    add_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    mileage = models.IntegerField(default=0)
    with_photo = models.BooleanField(default=True, null=True, blank=True)
    volume = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    condition = models.CharField(max_length=32)
    customs = models.CharField(max_length=32)
    availability = models.BooleanField()
    body = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    registration = models.CharField(max_length=32)
    owner=models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self):
        return self.car_name

    CHOICES_DRIVE = (
        ('задный', 'задный'),
        ('передный', 'передный'),
        ('полный', 'полный')
    )
    drive = models.CharField(default='задный', max_length=16, choices=CHOICES_DRIVE)

    CHOICES_ENGINE = (
        ('бензин', 'бензин'),
        ('газ', 'газ'),
        ('дизель', 'дизель'),
        ('электрический', 'электрический')
    )
    engine = models.CharField(max_length=16, default='бензин', choices=CHOICES_ENGINE)
    GEAR_BOX = (
        ('автомат', 'автомат'),
        ('механика', 'механика')
    )
    gearbox = models.CharField(max_length=32, default='автомат', choices=GEAR_BOX)

    STEERING_WHEEL = (
        ('слева', 'слева'),
        ('справо', 'справо')
    )
    steering_wheel = models.CharField(max_length=32, default='слева', choices=STEERING_WHEEL)

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class CarPhotos(models.Model):
    car = models.ForeignKey(Car, related_name='cars', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='rating',
                                null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replace', on_delete=models.CASCADE,
                               null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car}-{self.stars}'


class FavoriteCar(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(FavoriteCar, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
