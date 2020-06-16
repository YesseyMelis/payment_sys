import json

import requests
from rest_framework import serializers

from payment_sys.app.bank.models import Application, Program, Blacklist, Borrower
from payment_sys.app.utils.exceptions import CustomValidationError
from datetime import datetime


def get_age(birth):
    current = datetime.now()
    birth_date = datetime.strptime(birth, '%y%m%d')
    return current.year - birth_date.year - ((current.month, current.day) < (birth_date.month, birth_date.day))


class ApplicationCreateAgeSumValidateSerializer(serializers.Serializer):
    uin = serializers.CharField()
    sum = serializers.FloatField()

    def validate(self, attrs):
        errors = {}
        program = Program.objects.first()
        age = get_age(attrs.get('uin')[:6])
        if attrs.get('sum') > program.max_sum or attrs.get('sum') < program.min_sum:
            errors["error"] = "Заявка не подходит по сумме"
        if age > program.max_age or age < program.min_age:
            errors["error"] = "Заемщик не подходит по возрасту"
        return errors


class ApplicationCreateBusinessValidateSerializer(serializers.Serializer):
    uin = serializers.CharField()
    sum = serializers.FloatField(required=False)

    def validate(self, attrs):
        errors = {}
        url = 'https://stat.gov.kz/api/juridical/gov/?bin={}&lang=ru'.format(attrs.get('uin'))
        response = requests.get(url=url)
        data = json.loads(response.text)
        if not data.get('success'):
            errors['error'] = "иин является ИП"
        return errors


class ApplicationCreateBlacklistValidateSerializer(serializers.Serializer):
    uin = serializers.CharField()
    sum = serializers.FloatField(required=False)

    def validate(self, attrs):
        errors = {}
        if Blacklist.objects.filter(uin=attrs.get('uin')).exists():
            errors['error'] = "Заемщик в черном списке"
        return errors


class ApplicationCreateSerializer(serializers.ModelSerializer):
    uin = serializers.CharField()
    sum = serializers.FloatField()

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        program = Program.objects.first()
        uin = validated_data.get('uin')
        birth_date = datetime.strptime(uin[:6], '%y%m%d')
        borrower = Borrower.objects.create(
            uin=validated_data.get('uin'),
            birth_date=birth_date
        )
        app = Application.objects.create(
            program=program,
            borrower=borrower,
            sum=validated_data.get('sum')
        )
        age_sum_ser = ApplicationCreateAgeSumValidateSerializer(data=validated_data)
        age_sum_ser.is_valid(raise_exception=False)
        if age_sum_ser.validated_data:
            error = age_sum_ser.validated_data.get('error')
            app.status = Application.FAILURE
            app.failure_description = error
            app.save()
            raise CustomValidationError(error, 404)
        business_ser = ApplicationCreateBusinessValidateSerializer(data=validated_data)
        business_ser.is_valid(raise_exception=False)
        if business_ser.validated_data:
            error = business_ser.validated_data.get('error')
            app.status = Application.FAILURE
            app.failure_description = error
            app.save()
            raise CustomValidationError(error, 404)
        blacklist_ser = ApplicationCreateBlacklistValidateSerializer(data=validated_data)
        blacklist_ser.is_valid(raise_exception=False)
        if blacklist_ser.validated_data:
            error = blacklist_ser.validated_data.get('error')
            app.status = Application.FAILURE
            app.failure_description = error
            app.save()
            raise CustomValidationError(error, 404)
        return app
