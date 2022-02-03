from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.teachers import Teacher
from ..serializers.teachers import TeacherSerializer

class TeacherView(APIView):
    # list all the teachers and also get a teacher
    def get(self, request, teacher_id=None):
        if teacher_id is None:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Teachers listed successfully'
            }
            return Response(response, status=200)
        
        else:
            # get a teacher
            teacher_qs = Teacher.objects.filter(id=teacher_id)
            # Raise error if the teacher does not exist
            if not teacher_qs.exists():
                response = {
                    'status': 'error',
                    'message': 'Teacher does not exist'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            teacher = teacher_qs.first()
            serializer = TeacherSerializer(teacher)
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Teacher retrieved successfully'
            }
            return Response(response, status=status.HTTP_200_OK)

    # create a new teacher
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Teacher created successfully'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            'status': 'error',
            'data': serializer.errors,
            'message': 'Teacher could not be created'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # update a teacher
    def patch(self, request, teacher_id=None):
        # check if id is provided
        if teacher_id is None:
            response = {
                'status': 'error',
                'message': 'Teacher id is required'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # check if teacher exists
        teacher_qs = Teacher.objects.filter(id=teacher_id)
        if not teacher_qs.exists():
            response = {
                'status': 'error',
                'message': 'Teacher does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        teacher = teacher_qs.first()
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Teacher updated successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        
        response = {
            'status': 'error',
            'data': serializer.errors,
            'message': 'Teacher could not be updated'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)