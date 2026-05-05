from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
import re


#############USER MODEL#################
########################################

##### FIRST_NAME VALIDATOR
def validate_first_name(value):
    name_obj = value.upper().strip()
    letter_count = 0
    errors = []
    if len(name_obj) < 3:
        errors.append('El nombre no puede tener menos de 3 caracteres')
    if len(name_obj) > 250:
        errors.append('El nombre es demasiado largo')
    if re.search(r'[^a-zA-ZñÑ\s]', name_obj):
        errors.append('El nombre no puede llevar caracteres especiales')
    for letter in name_obj:
        if letter.isalpha():
            letter_count += 1
    if letter_count < 3:
        errors.append('El nombre debe tener al menos 3 letras')
    if errors:
        raise serializers.ValidationError(errors)
    return name_obj

##### LAST_NAME VALIDATOR
def validate_last_name(value):
    last_name_obj = value.upper().strip()
    letter_count = 0
    errors = []
    if len(last_name_obj) < 3:
        errors.append('El apellido no puede tener menos de 3 caracteres')
    if len(last_name_obj) >250:
        errors.append('El apellido es demasiado largo')
    if re.search(r'[^a-zA-ZñÑ\s]', last_name_obj):
        errors.append('No se admiten caracteres especiales, ni numeros en el apellido ')
    for letter in last_name_obj:
        if letter.isalpha():
            letter_count += 1
    if letter_count < 3:
        errors.append('El apellido debe tener al menos 3 letras')
    if errors:
        raise serializers.ValidationError(errors)
    return last_name_obj

#### PASSWORD VALIDATOR
def validate_password(value):
        pass_obj = value
        errors = []
        if len(pass_obj) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-z]', pass_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-Z]', pass_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', pass_obj):
            errors.append('La contraseña debe tener al menos un número')
        if not re.search(r'[^a-zA-Z0-9]', pass_obj):
            errors.append('La contraseña debe tener al menos un caracter especial')
        if errors:
            raise serializers.ValidationError(errors)
        return pass_obj
 

 ################################################################################################



############################## PROFILE USER VALIDATORS #########################################


####BUSINESS NAME VALIDATOR
def validate_business_name( value):
    business_obj = value.upper().strip()
    errors = []
    if len(business_obj)< 3:
        errors.append('Razon social demasiado corta')
    if len(business_obj) > 254:
        errors.append('Razón social demasiado larga')
    if errors:
        raise serializers.ValidationError(errors)
    return business_obj

#####STREET NAME
def validate_street_name(value):
    street__obj = value.upper().strip()
    errors = []
    if len(street__obj)< 4:
        errors.append('Nombre de barrio/calle demasiado corto')
    if len(street__obj) > 255:
        errors.append('Nombre de calle demasiado largo')
    if errors:
        raise serializers.ValidationError(errors)
    return street__obj

####STREET NUMBER
def validated_street_number(value):
    str_number_obj = value.upper().strip()
    errors = []
    if not str_number_obj:
        errors.append('Porfavor ingresa la altura/número de tu calle/barrio')
    if len(str_number_obj) > 100:
        errors.append('Altura/Número, demasiado largo')
    if errors:
        raise serializers.ValidationError(errors)
    return str_number_obj

#####APARTAMENT
def validate_apartament(value):
    apart_obj = value.upper().strip()
    errors = []
    if len(apart_obj) > 255:
        errors.append('Porfavor ingrese información valida')
    if errors:
        raise serializers.ValidationError(errors)
    return apart_obj



        