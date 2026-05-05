from rest_framework import serializers
from QuickShipApp.domains.user.models.models import UserProfile, Province, City
from QuickShipApp.domains.pendingshipment.models import PendingShipment, Details, Data
from QuickShipApp.domains.pendingshipment.serializers.mixin import UpdatePendingShipmentDataMixin, RegisterPendingShipmentDetailMixin
from QuickShipApp.domains.pendingshipment.serializers import validator

"""

<--- ESTE MODULO SE ENCARGA DE ADMINISTRAR SERIALIZERS RELACIONADOS CON EL MODULO pendingshipmentmodels --->

"""

####UPDATE  PENDINGSHIPMENT DATA  SERIALIZER
class UpdatePendingShipmentData(UpdatePendingShipmentDataMixin,serializers.ModelSerializer):
    """
    Serializador para actualizar datos de origen, destino y destinatario.
    """
    id = serializers.ReadOnlyField()
    shipment_fk = serializers.PrimaryKeyRelatedField(read_only = True)
    origin_province = serializers.PrimaryKeyRelatedField(
        label = 'Provincia de origen',
        queryset = Province.objects.all(),
        required = True
        
    )
    origin_city = serializers.PrimaryKeyRelatedField(
        label = 'Ciudad de origen',
        queryset = City.objects.all(),
        required = True
        
    )
    origin_address = serializers.CharField(
        label = 'Domicilio de origen del paquete',
        style = {'placeholder':'Dirección desde que se envia el paquete'},
        trim_whitespace = True,
        required = True,
        validators = [validator.validate_origin_address],
        max_length = 255,
    )
    receiver = serializers.CharField(
        label = 'Nombre destinatario',
        style = {'placeholder':'Nombre del destinatario'},
        trim_whitespace = True,
        required = True,
        validators = [validator.validate_receiver],
        max_length = 255,
    )
    receiver_document = serializers.CharField(
        label = 'Número de documento',
        style = {'placeholder':'Documento del destinatario'},
        trim_whitespace = True,
        required = True,
        validators = [validator.validate_receiver_document],
        max_length = 20,
    )
    receiver_business_name = serializers.CharField(
        label = 'Razon social',
        style = {'placeholder':'Razon social del destinatario'},
        allow_null = True
    )
    receiver_number_phone = serializers.CharField(
        label = 'Número de celular',
        style = {'placeholder':'Escribir el número sin +54'},
        trim_whitespace = True,
        required = True,
        validators = [validator.validate_receiver_number_phone],
        max_length = 20,
    )
    receiver_email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Correo electronico del destinatario'},
        trim_whitespace = True,
        validators = [validator.validate_receiver_email],
        required = True,
        max_length = 255,
    )
    destination_province = serializers.PrimaryKeyRelatedField(
        label = 'Provincia del destinatario',
        queryset = Province.objects.all(),
        required = True
    )
    destination_city =serializers.PrimaryKeyRelatedField(
        label = 'Ciudad del destinatario',
        queryset = City.objects.all(),
        required = True
    )
    destination_address = serializers.CharField(
        label = 'Domicilio del destinatario',
        style = {'placeholder':'Domicilio del destinatario'},
        trim_whitespace = True,
        validators = [validator.validate_destination_address],
        required = True,
        max_length = 255,
    )
    destination_extrainfo = serializers.CharField(
        label = 'Información extra',
        style = {'placeholder':'Detalles para llegar'},
        trim_whitespace = True,
        allow_null = True
    )
    class Meta:
        model = Data
        fields = ['id','shipment_fk','origin_province', 'origin_city','origin_address', 'receiver', 'receiver_type_document',
                 'receiver_document','receiver_tax_condition','receiver_business_name','receiver_number_phone',
                 'receiver_email','destination_province','destination_city','destination_address','destination_extrainfo']

####LIST PENDINGSHIPMENTDATA SERIALIZER
class ListPendingShipmentData(serializers.ModelSerializer):
    """
    Serializador para lectura de datos de envío.
    """
    origin_province = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    destination_province = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()
    class Meta:
        model = Data
        fields = '__all__'
        read_only_fields = [f.name for f in Data._meta.get_fields()]

####REGISTER PENDINGSHIPMENTDETAIL

class RegisterPendingShipmentDetail(RegisterPendingShipmentDetailMixin, serializers.ModelSerializer):
    """
    Serializador para la carga de productos y dimensiones.
    """
    id = serializers.ReadOnlyField()
    shipment_fk = serializers.PrimaryKeyRelatedField(read_only = True)
    description = serializers.CharField(
        label = 'Descripción',
        style = {'placeholder':'Descripción del objeto'},
        required = True,
        
        validators =[validator.validate_description]
    )
    weight = serializers.DecimalField(
        label = 'Peso',
        style = {'placeholder':'Peso del producto (en kilos)'},
        required = True,
        max_digits=12,
        decimal_places=2,
        validators = [validator.validate_weight]
    )
    height = serializers.DecimalField(
        label = 'Altura',
        style = {'placeholder':'Altura del objeto (en centimetros)'},
        required = True,
        
        max_digits=12,
        decimal_places=2,
        validators =[validator.validate_height]
    )
    width = serializers.DecimalField(
        label = 'Ancho',
        style = {'placeholder':'Ancho del objeto (en centrimetros)'},
        required = True,
        
        max_digits=12,
        decimal_places=2,
        validators = [validator.validate_width]
    )
    length = serializers.DecimalField(
        label = 'Largo',
        style = {'placeholder':'Largo del objeto (en centimetros)'},
        required = True,
        
        max_digits=12,
        decimal_places=2,
        validators = [validator.validate_length]
    )
    quantity = serializers.IntegerField(
        label = 'Cantidad',
        style = {'placeholder':'Cantidad'}, 
        default = 1,
        validators = [validator.validate_quantity]
    )
    weight_price = serializers.SerializerMethodField( read_only = True)
    subtotal = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Details
        fields = ['id','shipment_fk','description','weight','height','width','length','quantity','weight_price','subtotal']
    ##WEIGHT PRICE METHOD VALIDATOR
    def get_weight_price(self,obj):
        return obj.get_weight_price()

    ##SUBTOTAL PRICE METHOD VALIDATOR
    def get_subtotal(self,obj):
        return obj.get_subtotal()

####LIST PENDINGSHIPMENTDETAILS SERIALIZER
class ListPendingShipmentDetail(serializers.ModelSerializer):
    """
    Serializador para el listado de productos en el borrador.
    """
    subtotal = serializers.SerializerMethodField( read_only = True)
    weight_price = serializers.SerializerMethodField( read_only = True)
   
    class Meta:
        model = Details
        fields = ['id', 'description', 'weight', 'height', 'width', 'length', 'quantity', 'weight_price', 'subtotal']
    ##WEIGHT PRICE METHOD VALIDATOR
    def get_weight_price(self,obj):
        return obj.get_weight_price()

    ##SUBTOTAL PRICE METHOD VALIDATOR
    def get_subtotal(self,obj):
        return obj.get_subtotal()
###PENDINGSHIPMENT SERIALIZER

class ListPendingShipment(serializers.ModelSerializer):
    """
    Serializador integral que une datos, productos y precio total del borrador.
    """
    user_fk = serializers.HiddenField(default = serializers.CurrentUserDefault())
    data_shipment = ListPendingShipmentData(source = 'data')
    detail_shipment = ListPendingShipmentDetail(source = 'details', many = True)
    total_price = serializers.ReadOnlyField(source = 'get_total_price')
    class Meta:
        model = PendingShipment
        fields = ['user_fk', 'data_shipment','detail_shipment','total_price']
