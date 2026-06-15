from django.db import transaction
from django.db import models
from accounts.models.users import User
from django.core.validators import MinValueValidator

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.user} | {self.balance}"

    @transaction.atomic
    def deposit(self, amount):
        self.balance = amount
        # Implement deposit logic here
        self.save()
        return self

    @transaction.atomic
    def withdraw(self, amount):
        self.balance = amount
        # Implement withdraw logic here
        self.save()
        return self
