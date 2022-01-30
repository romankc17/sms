
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Class, Batch, Section
from .serializers import ClassSerializer, BatchSerializer, SectionSerializer


class BatchView(APIView):
    # List all the batches and the classes in each batch
    def get(self, request):
        batches = Batch.objects.all()
        serializer = BatchSerializer(batches, many=True, context={'request': request})
        
        return Response(serializer.data)