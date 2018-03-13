"""Save code from csv to DB"""
from buttons.models import Code
import csv



def corp_code_scraper():
	code_db = Code.objects.all()
	code_db.delete()

	create_code()


def create_code():

	with open('apis/data.csv') as datafile:
		reader = csv.reader(datafile)

		for row in reader:
			Code.objects.create(
				corp_name = row[1],
				corp_code = row[0]
				)


# Update corporate code to DB
corp_code_scraper()