from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

KIND = (
    ('B', 'Buy'),
    ('S', 'Sell'),
    ('T', 'Trade')
)

class Addon(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('addons_detail', kwargs={'pk': self.id})

class Coin(models.Model):
  name = models.CharField(max_length=100)
  condition = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  addons = models.ManyToManyField(Addon)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'coin_id': self.id})

  def offered_for_today(self):
    return self.offer_set.filter(date=date.today()).count() >= len(MEALS)

class Offer(models.Model):
  date = models.DateField('offer date')
  kind = models.CharField(
    max_length=1,
    choices=KIND,
    default=KIND[0][0]
  )
  coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_kind_display()} on {self.date}"

  # change the default sort
  class Meta:
    ordering = ['-date']
