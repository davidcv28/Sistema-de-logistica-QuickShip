from rest_framework import serializers
from QuickShipApp.domains.user.models import UserProfile
from QuickShipApp.domains.user.serializers.mixins_logic import validate_document_format, validate_tax_conditions
from QuickShipApp.domains.pendingshipment.models import PendingShipment, Data
from django.contrib.auth.models import User
from django.db import transaction
import re
####USER SERIALIZER VALIDATION####
###########################################
class MixinUserValidation:
    """
    Este mixin se encarga de validar campos para los serializers del model User

    """
    #email
    def validate_email(self, value):
        email_obj = value.lower().strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        allow_domains = ['@hotmail.com','@gmail.com', '@yahoo.com','@outlook.com','@live.com']
        domain_exists = False
        errors = []
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El correo ingresado ya se encuentra en uso')
        if len(email_obj) > 250:
            errors.append('Correo electronico no valido')
        for domain in allow_domains:
            if email_obj.endswith(domain):
                domain_exists = True
                break
        if not domain_exists:
            errors.append('El dominio ingresado no es valido')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj

    #username
    def validate_username(self, value):
        user_obj = value.strip()
        queryset = User.objects.filter(username__iexact = user_obj)
        errors = []
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de usuario ingresado ya esta en uso')
        if len(user_obj) < 4:
            errors.append('El nombre de usuario debe tener al menos 4 caracteres')
        if len(user_obj)>60:
            errors.append('Nombre ed usuario demasiado largo')
        if re.search(r'[\s]', user_obj):
            errors.append('El nombre de usuario no puede llevar espacios')
        if errors:
            raise serializers.ValidationError(errors)
        return user_obj
    
######USER REGISTER SERIALIZER METHODS #########
class MixinRegisterUserSerializerMethod:
        """
        Este mixin se encarga del metodo de registro de usuarios

        """
        def validate(self, attrs):
            password1 = attrs.get('password')
            password2 = attrs.get('password2')
            errors = {}
            if password1 != password2:
                errors['password2'] = 'Las contraseñas no coinciden'
            if errors:
                raise serializers.ValidationError(errors)
            attrs.pop('password2')
            return attrs
        def create(self, validated_data):
            with transaction.atomic():
                user= User.objects.create_user(
                    first_name = validated_data['first_name'],
                    last_name = validated_data['last_name'],
                    email= validated_data['email'],
                    username = validated_data['username'],
                    password = validated_data['password']          
                )
                UserProfile.objects.create(user = user)
                cartshipment =PendingShipment.objects.create(user_fk = user)
                Data.objects.create(shipment_fk = cartshipment)
                return user

######USER UPDATE PASSWORD SERIALIZER
"""
Mixin encargado de actualizar la contraseña del usuario

"""
class MixinUpdatePasswordMethod:
    def validate(self, attrs):
        oldpassword = attrs.get('old_password')
        newpassword = attrs.get('new_password')
        confirmpassword = attrs.get('confirm_password')
        user = self.context.get('request').user
        errors = {}
        if not oldpassword:
            errors['old_password'] = 'Porfavor ingrese la contraseña actual'
        if not newpassword:
            errors['new_password'] = 'Porfavor ingrese la nueva contraseña'
        if not confirmpassword:
            errors['confirm_password'] = 'Porfavor confirme la contraseña'
        if not user.check_password(oldpassword):
            errors['old_password'] = 'La contraseña actual es incorrecta'
        if oldpassword == newpassword:
            errors['new_password'] = 'Porfavor , ingresa una contraseña distinta a la actual'
        if newpassword != confirmpassword:
            errors['confirm_password'] = 'Las contraseñas no coinciden'
        if errors:
            raise serializers.ValidationError(errors)
        attrs.pop('old_password', None)
        attrs.pop('confirm_password', None)
        return attrs
    
    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save()
        return user
    



###############################################################
####################VALIDATIONS PROFILEUSER ###################
###############################################################


####USERPROFILE VALIDATIONS MIXINS
"""
Este mixin se encarga solamente de validar los campos del model UserProfile

"""
class MixinProfileUserValidation:
    def validate_document(self, value):
        doc_obj = value.strip()
        queryset = UserProfile.objects.filter(document__iexact = doc_obj)
        errors = []
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('El documento ingresado ya esta en uso')
        if re.search(r'[^0-9]', doc_obj):
            errors.append('Solo se admiten números')
        if errors:
            raise serializers.ValidationError(errors)
        return doc_obj
    def validate_phone_number(self, value):
        number_obj = value
        queryset = UserProfile.objects.filter(phone_number__iexact = number_obj)
        errors = []
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El número de telefono ingresado ya esta en uso')
        if len(number_obj) != 10:
            errors.append('Número de telefono no valido')
        if re.search(r'[^0-9]', number_obj):
            errors.append('Solo se admiten números')
        if errors:
            raise serializers.ValidationError(errors)
        return f'+54{number_obj}'
    
    def validate(self, attrs):
        #////////DOCUMENTS VALIDATION/////////#
        type_doc_obj = attrs.get('type_document')
        doc_obj = attrs.get('document')
        tax_obj = attrs.get('tax_condition')
        business_obj = attrs.get('business_name')
        errors = {}
        type_format_document = validate_document_format(type_doc_obj, doc_obj)
        type_tax_condition = validate_tax_conditions(type_doc_obj, tax_obj, business_obj)
        if type_format_document:
            errors |= type_format_document
        if type_tax_condition:
            errors |= type_tax_condition
        #////////CITY & PROVINCE VALIDATION ////////#
        city_obj = attrs.get('city_fk')
        attrs['zipcode'] = city_obj.zipcode
        province_obj = attrs.get('province_fk')
        if  city_obj not in province_obj.cities.all():
            errors['city_fk'] = f'La ciudad seleccionada no pertenece a la provincia de {province_obj.name_province}'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
     
    

  
            
    
    




    