from django import urls
from django.urls import path, include
from rest_framework import routers
#USERS
from QuickShipApp.domains.user.viewset import ListUserViewSet, RegisterUserViewSet, UpdateUserViewSet
#PENDINGN SHIPMENT
from QuickShipApp.domains.pendingshipment.viewset import (PendingShipmentViewSet)
#SHIPPING
from QuickShipApp.domains.shipping.viewset import RegisterShippingViewSet, ListShippingViewSet, ListStatusShippingViewSet
router = routers.DefaultRouter()
########################
#####USER ENDPOINTS#####
########################
"""
<----Aqui se registraran todos los endpoint pertenecientes a los model User y UserProfile---->

"""
#REGISTER USER
router.register(r'add_user', RegisterUserViewSet, basename='Register_user')
#LIST USER
router.register(r'list_users', ListUserViewSet, basename='List_users' )
#UPDATE USER
router.register(r'update_user', UpdateUserViewSet, basename='Update_users')
"""
<----Aqui se registraran todos los endpoint pertenecientes al modulo pendingshipment---->

"""
#PENDIGNSHIPMENT
router.register(r'pendingshipment', PendingShipmentViewSet, basename='PendingShipment_user')


"""

<--- Aqui se registraran todos los endpoints pertenecientes al modulo shiping --->

"""
#REGISTER SHIPPING
router.register(r'register_shipping', RegisterShippingViewSet, basename='Register_shipping')
#LIST SHIPPING
router.register(r'list_shipping', ListShippingViewSet, basename='List_shipping' )
#LIST STATUS SHIPPING
router.register(r'list_status', ListStatusShippingViewSet , basename='list_status')
urlpatterns = [


    path('', include(router.urls))
]
