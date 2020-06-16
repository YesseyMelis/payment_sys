from django.db import models


class Program(models.Model):
    min_sum = models.DecimalField(max_digits=56, decimal_places=4, blank=True, null=True)
    max_sum = models.DecimalField(max_digits=56, decimal_places=4, blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'programs'


class Borrower(models.Model):
    uin = models.CharField(max_length=191)
    birth_date = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        db_table = 'borrower'


class Application(models.Model):
    FAILURE = 'failure'
    SUCCESS = 'success'
    STATUS_CHOICES = (
        (FAILURE, 0),
        (SUCCESS, 1)
    )
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)
    borrower = models.ForeignKey(Borrower, on_delete=models.DO_NOTHING)
    sum = models.DecimalField(max_digits=56, decimal_places=4, blank=True, null=True)
    status = models.CharField(max_length=191, blank=True, null=True, choices=STATUS_CHOICES)
    failure_description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'applications'


class Blacklist(models.Model):
    uin = models.CharField(max_length=191)

    objects = models.Manager()

    class Meta:
        db_table = 'blacklist'
