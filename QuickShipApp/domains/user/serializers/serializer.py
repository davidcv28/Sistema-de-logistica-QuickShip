from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from QuickShipApp.domains.user.models.models import Province, City, UserProfile
from QuickShipApp.domains.user.serializers.mixin import (MixinUserValidation, MixinRegisterUserSerializerMethod,
 MixinUpdatePasswordMethod, MixinProfileUserValidation)
from QuickShipApp.domains.user.serializers import validator


#####LIST PROFILE USER SERIALIZER

"""
<----Serializer encargado de listar datos de UserProfile---->

"""
class ListProfileUser(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



#########################################################
################USER MODEL SERIALIZERS ##################
#########################################################
#####LIST USER SERIALIZER

"""
Serializer para listar los usuarios

"""
class ListUser(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    data = ListProfileUser(source='profile')
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name', 'email', 'data']
####REGISTER USER SERIALIZER
"""
<----Este serializer se encarga del
     registro de los usuarios ---->
"""
class RegisterUser(MixinRegisterUserSerializerMethod,MixinUserValidation, serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(
        label = 'Nombre',
        style ={'placeholder':'Escribe tu nombre'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 250,
        validators = [validator.validate_first_name]
    )
    last_name = serializers.CharField(
        label = 'Apellido/s',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 250,
        validators = [validator.validate_last_name]
    )
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Ejemplo@hotmail.com'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 250,
    )
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 60
    )
    password = serializers.CharField(
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 100,
        validators = [validator.validate_password]
    )
    password2 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Escribe de nuevo contraseña', 'input_type':'password'},
        required = True,
        write_only = True,
        trim_whitespace = True,
        max_length = 100
    )
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','username','password','password2']
        


####UPDATE DATA USER SERIALIZER
"""
 <----Este serializer se encarga exclusivamente de
         actualizar los datos del model user ---->
"""
class UpdateDataUser(MixinUserValidation,serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(
        label = 'Nombre',
        style = {'placeholder':'Escribe tu nombre'},
        required = True,
        trim_whitespace = True,
        max_length = 250,
        validators = [validator.validate_first_name]
    )
    last_name = serializers.CharField(
        label = 'Apellido/s',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        trim_whitespace = True,
        validators = [validator.validate_last_name]
    )
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Escibe tu correo electronico'},
        required = True,
        trim_whitespace = True,
        max_length = 255
    )
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','email']

####UPDATE PASSWORD SERIALIZER
"""
<----Este serializer se encarga de actualizar
     la contraseña del usuario---->

"""
class UpdatePassword(MixinUpdatePasswordMethod, serializers.Serializer):
    old_password = serializers.CharField(
        label = 'Contraseña actual',
        style = {'placeholder':'Escribe tu contraseña actual', 'input_type':'password'},
        required = True,
        write_only = True,
        max_length = 100
    )
    new_password = serializers.CharField(
        label = 'Nueva contraseña',
        style = {'placeholder':'Escribe tu nueva contraseña', 'input_type':'password'},
        required = True,
        write_only = True,
        max_length = 100,
        validators = [validator.validate_password]
    )
    confirm_password = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Escribe tu nueva contraseña de nuevo', 'input_type':'password'},
        required = True,
        write_only = True,
        max_length = 100
    )
##################################
####UPDATE PROFILEUSER SERIALIZER#
##################################


####UPDATE USER PROFILE
"""
<----Serializer encargado del update de profileuser---->

"""
class UpdateProfileUser(MixinProfileUserValidation,serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    document = serializers.CharField(
        label = 'Número de documento',
        style = {'placeholder':'Escribe tu número de docuemnto'},
        required = True,
        trim_whitespace = True,
        max_length = 20
    )
    business_name = serializers.CharField(
        label = 'Razon Social',
        style = {'placeholder':'Razon social'},
        trim_whitespace = True,
        max_length = 255,
        allow_null = True,
    )
    phone_number = serializers.CharField(
        label = 'Número de celular',
        style = {'placeholder':'Número de celular, sin +54'},
        required = True,
        trim_whitespace = True,
        max_length = 20
    )
    province_fk = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar Provincia',
        queryset = Province.objects.all(),
        required = True
    )
    city_fk = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar ciudad',
        queryset = City.objects.all(),
        required = True
    )
    zipcode = serializers.ReadOnlyField()
    street_name = serializers.CharField(
        label = 'Nombre de calle/barrio',
        style = {'placeholder':'Escribe el nombre de tu calle o barrio'},
        required = True,
        trim_whitespace = True,
        max_length = 255
    )
    street_number = serializers.CharField(
        label = 'Altura/Número',
        style = {'placeholder':'Altura o Número'},
        required = True,
        trim_whitespace = True,
        max_length = 100
    )
    apartament = serializers.CharField(
        label = 'Departamento(opcional)',
        style = {'placeholder':'ej, piso, puerta'},
        allow_null = True,
        trim_whitespace = True,
        max_length = 255
    )
    extra_info = serializers.CharField(
        label = 'Información extra (opcional)',
        style = {'placeholder':'Puedes dar detalles para llegar a tu domicilio'},
        trim_whitespace = True,
        max_length = 255,
        allow_null = True,
    )
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'type_document','document','tax_condition','business_name',
                  'phone_number','province_fk','city_fk','zipcode','street_name','street_number',
                  'apartament','extra_info']