
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Class, Batch, Section
from .serializers import ClassSerializer, BatchSerializer, SectionSerializer


class BatchView(APIView):
    # List all the batches and the classes in each batch
    def get(self, request, batch_year=None):
        if batch_year is None:
            batches = Batch.objects.all()
            batches_serializer = BatchSerializer(batches, many=True, context={'request': request})
            
            response = {
                "status": "success",
                "data": batches_serializer.data,
                "messages": "Batches retrieved successfully"          
            }

            return Response(response, status=status.HTTP_200_OK)

        else:
            batch_qs = Batch.objects.filter(year=batch_year)
            if not batch_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Batch not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            batch_serializer = BatchSerializer(batch_qs[0], context={'request': request})
            response = {
                "status": "success",
                "data": batch_serializer.data,
                "messages": "Batch retrieved successfully"
            }
            return Response(response, status=status.HTTP_200_OK)



    # Create a new batch
    def post(self, request, batch_year=None):
        if batch_year is None:        
            serializer = BatchSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "data": serializer.data,
                    "messages": "Batch created successfully"
                }
                return Response(response, status=status.HTTP_201_CREATED)

            response = {
                "status": "error",
                "data": serializer.errors,
                "messages": "Batch creation failed"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {
                "status": "error",
                "data": {},
                "messages": "Mehtod not allowed"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # Update a batch
    def put(self, request, batch_year=None):
        if batch_year is not None:
            batch_qs = Batch.objects.filter(year=batch_year)
            if not batch_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Batch not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            batch = batch_qs[0]
            serializer = BatchSerializer(batch, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "data": serializer.data,
                    "messages": "Batch updated successfully"
                }
                return Response(response, status=status.HTTP_200_OK)

            response = {
                "status": "error",
                "data": serializer.errors,
                "messages": "Batch update failed"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {
                "status": "error",
                "data": {},
                "messages": "Mehtod not allowed"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def delete(self, request, batch_year=None):
        if batch_year is not None:
            batch_qs = Batch.objects.filter(year=batch_year)
            if not batch_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Batch not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            batch_qs.delete()
            response = {
                "status": "success",
                "data": {},
                "messages": "Batch deleted successfully"
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                "status": "error",
                "data": {},
                "messages": "Mehtod not allowed"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ClassView(APIView):
    # Delete a class
    def delete(self, request, batch_year=None, class_name=None):
        class_qs = Class.objects.filter(batch__year=batch_year, name=class_name)
        if not class_qs.exists():
            response = {
                "status": "error",
                "data": {},
                "messages": "Class not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        class_qs.delete()
        response = {
            "status": "success",
            "data": {},
            "messages": "Class deleted successfully"
        }
        return Response(response, status=status.HTTP_200_OK)

    # List all the classes in a batch
    def get(self, request, batch_year=None):
        if batch_year is not None:
            batch_qs = Batch.objects.filter(year=batch_year)
            if not batch_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Class not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            classes = Class.objects.filter(batch=batch_qs[0])
            classes_serializer = ClassSerializer(classes, many=True, context={'request': request})
            response = {
                "status": "success",
                "data": classes_serializer.data,
                "messages": "Classes retrieved successfully"
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                "status": "error",
                "data": {},
                "messages": "Mehtod not allowed"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        

class SectionView(APIView):
    # Delete a section
    def delete(self, request, batch_year=None, class_name=None, section_name=None):
        section_qs = Section.objects.filter(class__batch__year=batch_year, class__name=class_name, name=section_name)
        if not section_qs.exists():
            response = {
                "status": "error",
                "data": {},
                "messages": "Section not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        section_qs.delete()
        response = {
            "status": "success",
            "data": {},
            "messages": "Section deleted successfully"
        }
        return Response(response, status=status.HTTP_200_OK)

    # list the sections of the class in the batch
    def get(self, request, batch_year=None, class_name=None):
        if batch_year is not None and class_name is not None:
            batch_qs = Batch.objects.filter(year=batch_year)
            if not batch_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Batch not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            class_qs = Class.objects.filter(batch=batch_qs[0], name=class_name)
            if not class_qs.exists():
                response = {
                    "status": "error",
                    "data": {},
                    "messages": "Class not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            section_qs = Section.objects.filter(class_name=class_qs[0])


            section_serializer = SectionSerializer(section_qs, many=True, context={'request': request})
            response = {
                "status": "success",
                "data": section_serializer.data,
                "messages": "Section retrieved successfully"
            }
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                "status": "error",
                "data": {},
                "messages": "Mehtod not allowed"
            }
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
