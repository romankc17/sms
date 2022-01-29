from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from .serializers import AccountSerializer
from .models import Account

@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):   
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=201)
        
    
        
        