from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from QuickShipApp.domains.shipping.serializers import RegisterShipping, ListShipping, ListStatusViewShipping
from QuickShipApp.domains.shipping.models import Shipping, DetailShipping, DataShipping
from QuickShipApp.domains.shipping.filters import ShippingFilterSet
from django_filters.rest_framework import DjangoFilterBackend

"""
<--- Aquí se administran los viewsets de los serializers correspondientes al modelo Shipping --->

"""

####REGISTER SHIPPING VIEWSET
class RegisterShippingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Confirma el borrador y crea el envío oficial con su seguimiento.
    """
    serializer_class = RegisterShipping
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Shipping.objects.filter(user = self.request.user)
    def create(self, request):
        """
        Valida el borrador, genera el envío final y limpia el carrito.
        """
        serializer = self.get_serializer(data = request.data )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'Éxito':'El pedido se realizó con éxito'
            }, status=status.HTTP_200_OK
        )
####LIST SHIPPING VIEWSET
class ListShippingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Muestra el historial de todos los envíos hechos por el usuario.
    """
    serializer_class = ListShipping
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Shipping.objects.filter(user = self.request.user)
    
####LIST STATUS VIEWSET
class ListStatusShippingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Para consultar rápido el estado y código de seguimiento de los pedidos.
    """
    serializer_class = ListStatusViewShipping
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShippingFilterSet
    def get_queryset(self):
        shipping = Shipping.objects.filter(user = self.request.user)
        return shipping
    