from django.test import TestCase
from classes.models import Class, BatchedClass, Section

class ClassTestCase(TestCase):
    def setUp(self):
        self.class_1 = Class.objects.create(name='1')
        self.class_2 = Class.objects.create(name='2')
        self.class_3 = Class.objects.create(name='3')

    def test_class_creation(self):
        class_1 = Class.objects.get(name='1')
        class_2 = Class.objects.get(name='2')
        class_3 = Class.objects.get(name='3')
        self.assertEqual(class_1.name, '1')
        self.assertEqual(class_2.name, '2')
        self.assertEqual(class_3.name, '3')


class BatchedClassTestCase(TestCase):
    def setUp(self):   
        self.class_1 = Class.objects.create(name='1')
        self.class_2 = Class.objects.create(name='2')
        self.batch_2078 = BatchedClass.objects.create(year=2078)
        self.batch_2078.class_name.add(self.class_1)
        print(self.batch_2078.class_name.all())
        print(BatchedClass.objects.filter(class_name__id=1))

    def test_batched_class_creation(self):

        class_1 = Class.objects.get(name='1')
        print(class_1)
       
        