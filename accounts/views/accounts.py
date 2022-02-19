from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView


from accounts.serializers.accounts import AccountSerializer, CustomTokenObtainPairSerializer
from accounts.models.accounts import Account
from accounts.models.teachers import Teacher

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        teacher_qs = Teacher.objects.filter(email=email)
        if not teacher_qs.exists():
            response = {
                'status': 'error',
                'message': 'User does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        teacher = teacher_qs[0]
        data = {
            "username":teacher.phone,
            "email":email,
            "is_staff":True,
            "is_admin":False,
            "password":password
        }
        
        serializer = AccountSerializer(data=data)
        if not serializer.is_valid():
            response = {
                'status': 'error',
                'data': serializer.errors,
                'message': 'User could not be created'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()        
        return Response(serializer.data, status=201)
        
    
        
        