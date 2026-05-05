from QuickShipApp.domains.shipping.models import Shipping, ShippingStatus, DataShipping, DetailShipping
from QuickShipApp.domains.shipping.serializers.mixin import MixinShippingRegisterMethod
from rest_framework import serializers
"""
<--- En este módulo se administrarán los serializers correspondientes al modelo Shipping --->
"""

####LIST DETAIL SHIPPING SERIALIZER
class ListShippingDetail(serializers.ModelSerializer):

    description = serializers.ReadOnlyField()
    weight = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    length = serializers.ReadOnlyField()
    quantity = serializers.ReadOnlyField()
    weight_price = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    class Meta:
        model = DetailShipping
        fields = ['id', 'description', 'weight', 'height', 'width', 'length','quantity','weight_price','subtotal']

#####LIST DATA SHIPPING SERIALIZER
class ListShippingData(serializers.ModelSerializer):
     id = serializers.ReadOnlyField()
     #SENDER
     sender_name = serializers.ReadOnlyField()
     sender_type_document = serializers.ReadOnlyField()
     sender_document = serializers.ReadOnlyField()
     sender_tax_condition = serializers.ReadOnlyField()
     sender_business_name = serializers.ReadOnlyField()
     sender_email = serializers.ReadOnlyField()
     sender_number_phone = serializers.ReadOnlyField()
     #ORIGIN
     origin_province = serializers.ReadOnlyField()
     origin_city = serializers.ReadOnlyField()
     origin_zipcode = serializers.ReadOnlyField()
     origin_address = serializers.ReadOnlyField()
     #RECEIVER
     receiver_name = serializers.ReadOnlyField()
     receiver_type_document = serializers.ReadOnlyField()
     receiver_document = serializers.ReadOnlyField()
     receiver_tax_condition = serializers.ReadOnlyField()
     receiver_business_name = serializers.ReadOnlyField()
     receiver_email = serializers.ReadOnlyField()
     receiver_number_phone = serializers.ReadOnlyField()
     #DETINATION
     destination_province = serializers.ReadOnlyField()
     destination_city = serializers.ReadOnlyField()
     destination_zipcode = serializers.ReadOnlyField()
     destination_address = serializers.ReadOnlyField()
     destination_extra_info = serializers.ReadOnlyField()
     class Meta:
        model = DataShipping
        fields = [#SENDER
                  'shipping_fk','id','sender_name','sender_type_document',
                  'sender_document','sender_tax_condition','sender_business_name',
                  'sender_email', 'sender_number_phone', # Corregido el nombre del campo
                  #ORIGIN
                  'origin_province', 'origin_city','origin_zipcode','origin_address',
                  #RECEIVER
                  'receiver_name','receiver_type_document','receiver_document',
                  'receiver_tax_condition','receiver_business_name','receiver_email',
                  'receiver_number_phone',
                  #DESTINATION
                  'destination_province','destination_city','destination_zipcode',
                  'destination_address','destination_extra_info']


####LIST STATUS SHIPPING SERIALIZER
class ListStatusShipping(serializers.ModelSerializer):
  
    id = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    class Meta:
        model = ShippingStatus
        fields = [ 'id', 'status', 'updated_at']
    

####REGISTER SHIPPING SERIALIZER
class RegisterShipping(MixinShippingRegisterMethod,serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    id = serializers.ReadOnlyField() # Corregido el nombre del campo
    shipping_number = serializers.ReadOnlyField()
    tracking_code = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    shipping_price = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Shipping
        fields = ['user', 'id', 'shipping_number','tracking_code','created_at',
                  'shipping_price','total_price']
#####LIST SHIPPING SERIALIZER
class ListShipping(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault()) 
    id = serializers.ReadOnlyField()
    shipping_number = serializers.ReadOnlyField()
    tracking_code = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    data = ListShippingData(source='data_shipping',read_only = True)
    details = ListShippingDetail(source='details_shipping',read_only = True ,many = True)
    shipping_price = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Shipping
        fields = ['user', 'id', 'shipping_number','tracking_code','created_at',
                  'data', 'details','status', 'shipping_price','total_price']


#####LIST STATUS SHIPPING SERIALIZER
class ListStatusViewShipping(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    status = ListStatusShipping( read_only = True)
    tracking_code = serializers.ReadOnlyField()
    class Meta:
        model = Shipping
        fields = ['id', 'user', 'status', 'tracking_code']