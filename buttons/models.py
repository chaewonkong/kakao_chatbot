from django.db import models


class Index(models.Model):
	"""Store KOSPI and KOSDAQ Index"""
	id = models.AutoField(primary_key=True)
	market_name = models.CharField(max_length=30, default="")
	index = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.index


class Code(models.Model):
	id = models.AutoField(primary_key=True)
	corp_name = models.CharField(max_length=40, default="")
	corp_code = models.CharField(max_length=30, default="")

	def __str__(self):
		return self.corp_name
