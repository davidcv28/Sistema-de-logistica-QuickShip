from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from QuickShipApp import permission
from QuickShipApp.domains.pendingshipment.serializers.serializer import ListPendingShipment, UpdatePendingShipmentData, RegisterPendingShipmentDetail
from QuickShipApp.domains.user.models import Province, City, UserProfile
from QuickShipApp.domains.pendingshipment.models import PendingShipment, Data, Details

"""

<--- En este modulo administramos los viewsets pertenecientes al modulo pendingshipmentserializer --->

"""

####PENDING SHIPMENT VIEWSET

class PendingShipmentViewSet( viewsets.GenericViewSet):
    """
    Gestión del borrador de envío (datos y productos).
    """
    def get_serializer_class(self):
        if self.action == 'pendingshipmentview':
            return ListPendingShipment
        if self.action == "data_shipment":
            return UpdatePendingShipmentData
        if self.action == "details_shipment":
            return RegisterPendingShipmentDetail
    def get_queryset(self):
        if self.action == 'pendingshipmentview':
            return PendingShipment.objects.select_related('user_fk').filter(user_fk = self.request.user)
        if self.action == 'data_shipment':
            return Data.objects.select_related('shipment_fk').filter(shipment_fk__user_fk = self.request.user)
        if self.action == 'details_shipment':
            return Details.objects.select_related('shipment_fk').filter(shipment_fk__user_fk = self.request.user)
    def get_object(self):
        if self.action == 'pendingshipmentview':
            return PendingShipment.objects.select_related('user_fk').get(user_fk = self.request.user)
        if self.action == 'data_shipment':
            return Data.objects.select_related('shipment_fk').get(shipment_fk__user_fk = self.request.user)

    @action(detail=False, methods =['GET'], url_path='pendingshipmentview')
    def pendingshipmentview(self, request):
        """
        Visualizar el contenido completo del borrador actual.
        """
        obj_shipment = self.get_object()
        serializer = self.get_serializer(obj_shipment)
        return Response(
            serializer.data
        )
    @action(detail= False, methods=['PUT', 'PATCH'], url_path = 'data_shipment')
    def data_shipment(self,request):
        """
        Actualizar información de origen y destino del borrador.
        """
        obj_data = self.get_object()
        serializer = self.get_serializer(data = request.data, instance = obj_data, context = {'request':request}, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'Exito':'Datos registrados'
            }, status=status.HTTP_200_OK
        )
    @action(detail=False, methods=['POST','PUT','PATCH'], url_path='details_shipment')
    def details_shipment(self, request):
        """
        Registrar o actualizar productos dentro del borrador.
        """
        if request.method in ['PUT', 'PATCH']:
            detail_obj = Details.objects.select_related('shipment_fk').get(shipment_fk__user_fk = request.user)
            serializer = self.get_serializer(data = request.data, instance = detail_obj,partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(
                {
                    'exito':'Producto Actualizado'
                },status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'exito':'Producto registrado'
            }, status=status.HTTP_200_OK
        )
