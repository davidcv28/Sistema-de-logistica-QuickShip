from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from QuickShipApp.domains.user.models.models import UserProfile, Province, City
from QuickShipApp.domains.user.serializers.serializer import ListUser, RegisterUser, UpdateDataUser, UpdatePassword, UpdateProfileUser
from QuickShipApp.permission import UserAnonimousPermission


#####LIST USER VIEWSET
"""
<---- Viewset encargado de listar el model User ---->

"""
class ListUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ListUser
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


#####REGISTER USER VIEWSET

"""
<---- Viewset encargado de registrar Usuarios ---->

"""

class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterUser
    permission_classes = [UserAnonimousPermission]
    queryset = User.objects.all()
    def create(self, request):
        serializer = self.get_serializer(data = request.data, context = {'request':request} )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'Exito':'El registro fue exitoso'
            }, status=status.HTTP_200_OK
        )

#####UPDATE  USER VIEWSET
"""
<----Viewset encargado de actualizar datos del model User---->
"""
class UpdateUserViewSet( viewsets.GenericViewSet):
    """
    Maneja las actualizaciones de datos básicos, contraseña y perfil del usuario.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get_serializer_class(self):
        if self.action =='update_user':
            return UpdateDataUser
        if self.action =='update_password':
            return UpdatePassword
        if self.action == 'update_profile':
            return UpdateProfileUser
    def get_queryset(self):
        if self.action in ['update_user', 'update_password']:
            return User.objects.filter(id = self.request.user.id)
        return UserProfile.objects.select_related('user').filter(user = self.request.user)
    def get_object(self):
        if self.action == 'update_profile':
            return UserProfile.objects.select_related('user').get(user = self.request.user)
        return super().get_object()
    @action(detail = False, methods = ['put','patch', 'get'], url_path='update_user')
    def update_user(self, request):
        """
        Actualiza nombre, apellido o email del usuario.
        """
        if request.method == 'GET':
            serializer = self.get_serializer( request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(data = request.data, instance = request.user, context = {'request':request}, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'Exito':'Los datos se actualizaron satisfactoriamente'
            }, status=status.HTTP_200_OK
        )
    @action(detail = False, methods = ['POST'], url_path ='update_password')
    def update_password(self, request):
        """
        Permite al usuario cambiar su contraseña actual por una nueva.
        """
        serializer = self.get_serializer(data = request.data, instance = request.user, context ={'request':request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'Exito':'La contraseña se modifico satisfactoriamente'
            }, status=status.HTTP_200_OK
        )
    @action(detail = False, methods = ['get','put','patch'], url_path='update_profile')
    def update_profile(self, request):
        """
        Actualiza la info detallada del perfil (dirección, teléfono, doc, etc).
        """
        instance = self.get_object()
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        serializer = self.get_serializer(data = request.data, instance = instance, context = {'request':request}, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'exito':'Datos actualizados con exito'
            }, status=status.HTTP_200_OK
        )
    