from rest_framework import serializers
from QuickShipApp.domains.pendingshipment.models import PendingShipment, Details, Data
from QuickShipApp.domains.user.models.models import Province, City, UserProfile
import re

"""
Funciones de validación atómica para campos de envíos y paquetes.
"""

#####DATA SHIPMENT VALIDATORS######


##ORIGIN ADDRESS VALIDATOR
def validate_origin_address(value):
    """
    Revisa que la dirección de origen sea válida.
    """
    address_obj = value.upper().strip()
    letter_count = 0
    errors = []
    if len(address_obj) < 3:
        errors.append('Por favor ingrese un domicilio válido')
    if len(address_obj)> 255:
        errors.append('Domicilio demasiado largo')
    for letter in address_obj:
        if letter.isalpha():
            letter_count += 1
    if letter_count < 3:
        errors.append('El domicilio debe tener al menos 3 letras')
    if errors:
        raise serializers.ValidationError(errors)
    return address_obj

##RECEIVER VALIDATOR
def validate_receiver(value):
    """
    Valida que el nombre del que recibe solo tenga letras.
    """
    receiver_name_obj = value.upper().strip()
    errors = []
    if len(receiver_name_obj) < 4:
        errors.append('Nombre de destinatario demasiado corto')
    if len(receiver_name_obj) > 255:
        errors.append('Nombre de destinatario demasiado largo')
    if re.search(r'[^A-Za-zñÑ\s]', receiver_name_obj):
        errors.append('Sólo se admiten letras')
    if errors:
        raise serializers.ValidationError(errors)
    return receiver_name_obj

##RECEIVER DOCUMENT VALIDATOR
def validate_receiver_document(value):
    """
    Chequea que el documento sea numérico y tenga un largo correcto.
    """
    doc_rec_obj = value
    errors = []
    if len(doc_rec_obj) < 6 or len(doc_rec_obj) > 11:
        errors.append('Documento inválido')
    if re.search(r'[^0-9]', doc_rec_obj):
        errors.append('Sólo se admiten números')
    if errors:
        raise serializers.ValidationError(errors)
    return doc_rec_obj
##VALIDATE BUSINESS NAME
def validate_receiver_business_name(value):
    """
    Valida que la razón social no tenga símbolos raros.
    """
    business_obj = value.upper().strip()
    errors = []
    if len(business_obj) < 3 or len(business_obj) > 255:
        errors.append('Por favor ingrese un nombre válido')
    if re.search(r'[^A-Z0-9ÑÁÉÍÓÚ.&, \-\(\)]', business_obj):
        errors.append('Se ingresaron caracteres no válidos')
    if errors:
        raise serializers.ValidationError(errors)
    return business_obj
##RECEIVER NUMBER PHONE VALIDATOR
def validate_receiver_number_phone(value):
    """
    Valida que el celular tenga 10 dígitos.
    """
    number_phone_obj = value
    errors = []
    if len(number_phone_obj) != 10:
        errors.append('Número de celular inválido')
    if re.search(r'[^0-9]', number_phone_obj):
        errors.append('Sólo se admiten números')
    if errors:
        raise serializers.ValidationError(errors)
    return f'+54{number_phone_obj}'
##RECEIVER EMAIL
def validate_receiver_email(value):
    """
    Valida que el email sea de proveedores conocidos (Gmail, etc).
    """
    email_obj = value
    allow_domains = ['@gmail.com', '@hotmail.com', '@outlook.com', '@yahoo.com', '@live.com']
    domain_exists = False
    errors = []
    for domain in allow_domains:
        if email_obj.endswith(domain):
            domain_exists = True
            break
    if not domain_exists:
        errors.append('Dominio ingresado no válido')
    if errors:
        raise serializers.ValidationError(errors)
    return email_obj

##DESTINATION ADDRESS
def validate_destination_address(value):
    """
    Revisa que la dirección de destino sea válida.
    """
    address_obj = value.upper().strip()
    letter_count = 0
    errors = []
    if len(address_obj) < 4:
        errors.append('Domicilio demasiado corto')
    if len(address_obj) > 255:
        errors.append('Domicilio demasiado largo')
    for letter in address_obj:
        if letter.isalpha():
            letter_count += 1
    if letter_count < 3:
        errors.append('El domicilio debe tener al menos 3 letras')
    if errors:
        raise serializers.ValidationError(errors)
    return address_obj



#######DETAILS SHIPMENT VALIDATORS#########


##DESCRIPTION VALIDATOR
def validate_description(value):
    """
    Valida que la descripción del producto no sea muy corta.
    """
    description_obj = value.upper().strip()
    letter_count = 0
    errors = []
    if len(description_obj) < 3:
        errors.append('Descripción demasiado corta')
    if len(description_obj) > 255:
        errors.append('Descripción demasiado larga')
    for letter in description_obj:
        if letter.isalpha():
            letter_count += 1
    if letter_count < 3:
        errors.append('La descripción debe tener al menos 3 letras')
    if errors:
        raise serializers.ValidationError(errors)
    return description_obj

##WEIGHT VALIDATOR
def validate_weight(value):
    """
    Controla que el peso esté entre 0.5kg y 60kg.
    """
    w_obj = float(value)
    errors = []
    if w_obj < 0.5 or w_obj > 60:
        errors.append('El peso de este objeto no cumple con las condiciones del sistema')
    if errors:
        raise serializers.ValidationError(errors)
    return round(w_obj,2)

##HEIGHT VALIDATOR
def validate_height(value):
    """
    Valida que la altura esté dentro de los límites (0.3cm a 100cm).
    """
    h_obj = float(value)
    errors = []
    if h_obj < 0.3 or h_obj > 100:
        errors.append('La altura del objeto no cumple con las condiciones del sistema')
    if errors:
        raise serializers.ValidationError(errors)
    return round(h_obj,2)
##WIDTH VALIDATOR
def validate_width(value):
    """
    Valida que el ancho esté dentro de los límites (0.3cm a 100cm).
    """
    w_obj = float(value)
    errors =[]
    if w_obj < 0.3 or w_obj > 100:
        errors.append('El ancho del objeto no cumple con las condiciones del sistema')
    if errors:
        raise serializers.ValidationError(errors)
    return round(w_obj,2)

##LENGTH VALIDATOR
def validate_length(value):
    """
    Valida que el largo no supere los 270cm.
    """
    l_obj = float(value)
    errors =[]
    if l_obj < 0.3 or l_obj > 270:
        errors.append('El largo del objeto no cumple con las condiciones del sistema')
    if errors:
        raise serializers.ValidationError(errors)
    return round(l_obj,2)

##QUANTITY VALIDATOR
def validate_quantity(value):
    """
    Controla que la cantidad sea entre 1 y 10 bultos.
    """
    q_obj = value
    errors = []
    if q_obj < 1:
        q_obj = 1
    if q_obj >10:
        errors.append('Se superó el límite permitido de objetos')
    if errors:
        raise serializers.ValidationError(errors)
    return q_obj
