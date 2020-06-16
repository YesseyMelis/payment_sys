from django.contrib import admin

from app.bank.models import Program, Borrower, Application, Blacklist

models = (Program, Borrower, Application, Blacklist)

admin.site.register(models)
