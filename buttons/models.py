from django.db import models


class Index(models.Model):
	"""Store KOSPI and KOSDAQ Index"""

	market_name = models.CharField(max_length=30, default="")
	index = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.index
