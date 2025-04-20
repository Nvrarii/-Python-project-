from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# 📦 1. **User (Пользователь)**
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name

# 📦 2. **Gym (Спортзал)**
class Gym(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    contact_phone = models.CharField(max_length=20)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# 📦 3. **Hall (Зал внутри спортзала)**
class Hall(models.Model):
    gym = models.ForeignKey(Gym, related_name='halls', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    type = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.name} ({self.gym.name})'

# 📦 4. **Schedule (Расписание работы зала)**
class Schedule(models.Model):
    hall = models.ForeignKey(Hall, related_name='schedules', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])])
    open_time = models.TimeField()
    close_time = models.TimeField()
    
    def __str__(self):
        return f'{self.hall.name} - {self.get_day_of_week_display()}'

# 📦 5. **Booking (Бронирование)**
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, related_name='bookings', on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.name} - {self.hall.name} on {self.booking_date}'

# 📦 6. **Payment (Оплата)**
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    
    booking = models.ForeignKey(Booking, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f'{self.booking.user.name} - {self.amount} ({self.status})'
