from django.db import models

# class Journal(models.Model):
#     pub_date = models.DateTimeField('date published')
#     origin = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.origin + ' - ' + str(self.pub_date.day) + '/' + str(self.pub_date.month) + '/' + str(self.pub_date.year)
#

# TODO must add more details to this class, with more structure.
# class Separata(models.Model):
#     journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return doc_text[0:20]
