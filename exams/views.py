from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Exam, Subject
from classes.models import Batch, Class

from .serializers import ExamSerializer


class ExamListView(APIView):
    # get all exams of the class
    def get(self, request, batch_year, class_name, format=None):
        # get the class from the batch_year and class_name

        # check if the batch exists
        batch_qs = Batch.objects.filter(year=batch_year)
        if not batch_qs.exists():
            return Response(
                {
                    'message': 'Batch with the year {} does not exist'.format(batch_year),
                    'status': 'error'                    
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # check if the class exists
        class_qs = Class.objects.filter(name=class_name, batch=batch_qs[0])
        if not class_qs.exists():
            return Response(
                {
                    'message': 'Class with the name {} does not exist'.format(class_name),
                    'status': 'error'                    
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # get the exams of the class
        exams = Exam.objects.filter(class_name=class_qs[0])
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)
