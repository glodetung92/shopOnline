from django.db import models
from autoslug import AutoSlugField



class Category(models.Model):
	title = models.CharField(max_length=300)
	primaryCategory = models.BooleanField(default=False)

	def __str__(self):
		return self.title



class Product(models.Model):
	mainimage = models.ImageField(upload_to='images/products/', blank=True)
	name = models.CharField(max_length=300)
	slug = AutoSlugField(populate_from='name')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
	detail_text = models.TextField(max_length=200, verbose_name='Detail Text')
	price = models.FloatField()

	def __str__(self):
		return self.name


