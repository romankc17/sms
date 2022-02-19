from rest_framework import serializers

from ..models.students import Student, StudentBatchRollNumber

from classes.models import Batch, Class, Section

"""
Student Batches and Roll Numbers Serializer
"""
class StudentBatchRollNumberSerializer(serializers.ModelSerializer):
    batch_year = serializers.IntegerField(source='section.class_name.batch.year')
    class_name = serializers.CharField(source='section.class_name.name')
    section_name = serializers.CharField(source='section.name')

    class Meta:
        model = StudentBatchRollNumber
        fields = (
            'roll_no',
            'batch_year',
            'class_name',
            'section_name',
        )



"""
Student Serializer
"""
class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # for writing the batch details
    # and roll number of that student at that batch
    batch_year = serializers.IntegerField(write_only=True)
    class_name = serializers.CharField(write_only=True)
    section_name = serializers.CharField(write_only=True)
    roll_no = serializers.IntegerField(write_only=True)
    
    # address = AddressSerializer(many=False)
    # for read only of the roll number and the respective batches
    student_batch_roll_numbers = StudentBatchRollNumberSerializer(read_only=True, many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add address field to the fields
        # self.fields['address'] = AddressSerializer(many=False)
        print(kwargs)

    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'student_batch_roll_numbers',
            'village',
            'ward_no',
            'tole',
            'dob',
            'parent_name',
            'parent_contact',
            'image',
            'gender',
            'batch_year',
            'class_name',
            'section_name',            
            'roll_no',         
        )
        depth = 3

    # Check if the batch with the given batch year exists
    def validate_batch_year(self, value):
        batch = Batch.objects.filter(year=value)
        if not batch.exists():
            print('raisein')
            raise serializers.ValidationError('Batch does not exist')

        return value

    # Check if the class with the given value exists
    def validate_class_(self, value):
        class_ = Class.objects.filter(
            name=value,
            batch=Batch.objects.get(year=self.initial_data['batch_year'])
        )           
        if not class_.exists():
            raise serializers.ValidationError('Class does not exist')

        return value

    # Check if the section with the given value exists
    def validate_section(self, value):
        section = Section.objects.filter(
            name=value,
            class_name=Class.objects.get(
                name=self.initial_data['class_name'],
                batch=Batch.objects.get(year=self.initial_data['batch_year'])
            )
        )
        if not section.exists():
            raise serializers.ValidationError('Section does not exist')
        
        return value

    # Check if the roll number is already taken
    def validate_roll_no(self, value):
        if self.validate_batch_year(self.initial_data['batch_year']) and self.validate_class_(self.initial_data['class_name']) and self.validate_section(self.initial_data['section_name']):
        # get the section object
            section = Section.objects.get(
                name=self.initial_data['section_name'],
                class_name=Class.objects.get(
                    name=self.initial_data['class_name'],
                    batch=Batch.objects.get(year=self.initial_data['batch_year'])
                )
            )

            # check if the roll number is already taken
            if StudentBatchRollNumber.objects.filter(
                roll_no=value,
                section=section,
            ).exists():
                raise serializers.ValidationError('Roll number already taken')

        return value

    # customizing create to create student with address
    def create(self, validated_data):
        # Populating roll number
        roll_no = validated_data.pop('roll_no')
        # Populating batch year, class and section 
        batch_year = validated_data.pop('batch_year')
        class_name = validated_data.pop('class_name')
        section_name = validated_data.pop('section_name')

        # creating a student
        student = Student(**validated_data)
        student.save()

        # add student to section
        section = Section.objects.get(
            name=section_name,
            class_name=Class.objects.get(
                name=class_name,                
                batch=Batch.objects.get(year=batch_year)
            ),
        )
        student.sections.add(section)

        # add student roll no
        StudentBatchRollNumber.objects.create(
            student=student,
            section=section,
            roll_no=roll_no
        )
       


        return student

    # customizing update to update student with address
    def update(self, instance, validated_data):        
        # updating student
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

        