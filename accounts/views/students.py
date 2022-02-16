from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from ..models.students import Student
from ..serializers.students import StudentSerializer

from classes.models import Batch, Class, Section


class StudentView(APIView):
    # list all the students and get a student by id
    def get(self, request, student_id=None):
        # get a student if id is provided in url
        if student_id:
            # check if the student with given id exists
            student_qs = Student.objects.filter(id=student_id)
            if student_qs.exists():
                serializer = StudentSerializer(student_qs.first())
                response = {
                    'status': 'success',
                    'data': serializer.data,
                    'message': 'Student retrieved successfully'
                }
                return Response(response, status=status.HTTP_200_OK)

            response = {
                'status': 'error',
                'message': 'Student with given id does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # get all the students if id not provided in url
        else:

            # get the students with the given query params
            params = request.query_params

            student_qs = Student.objects.all()
            
            if 'batch' in params:
                batch_year = params['batch']

                # get all the classes id within the given batch
                classes = Batch.objects.filter(year=int(batch_year)).values_list('classes', flat=True)
                sections = Class.objects.filter(id__in=classes).values_list('sections', flat=True)

                student_qs = student_qs.filter(sections__in=sections)

            if 'batch' in params and'class' in params:
                class_name = params['class']
                classes_id_list = list(classes)
                sections = Class.objects.filter(id__in=classes_id_list, name=class_name).values_list('sections', flat=True)

                student_qs = student_qs.filter(sections__in=sections)

            if 'batch' in params and 'class' in params and 'section' in params:
                section_name = params['section']
                sections_id_list = list(sections)
                sections = Section.objects.filter(id__in=sections_id_list, name=section_name).values_list('id', flat=True)

                student_qs = student_qs.filter(sections__in=sections)

            # students = Student.get_latest_batch_students()
            serializer = StudentSerializer(student_qs, many=True)
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Students retrieved successfully'
            }
            return Response(response, status=status.HTTP_200_OK)

    # create a new student
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'data': serializer.data,
                'message': 'Student created successfully'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'status': 'error',
            'message': 'Student could not be created',
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # update a student
    def put(self, request, student_id):
        student_qs = Student.objects.filter(id=student_id)
        if student_qs.exists():
            student = student_qs.first()
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 'success',
                    'data': serializer.data,
                    'message': 'Student updated successfully'
                }
                return Response(response, status=status.HTTP_200_OK)

            response = {
                'status': 'error',
                'message': 'Student could not be updated',
                'errors': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'status': 'error',
            'message': 'Student with given id does not exist'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    # delete a student
    def delete(self, request, student_id):
        student_qs = Student.objects.filter(id=student_id)
        if student_qs.exists():
            student = student_qs.first()
            student.delete()
            response = {
                'status': 'success',
                'message': 'Student deleted successfully'
            }
            return Response(response, status=status.HTTP_200_OK)

        response = {
            'status': 'error',
            'message': 'Student with given id does not exist'
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)


