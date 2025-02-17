from django.test import TestCase
from personal.models import User

# Create your tests here.
class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Run once to set uo non-modified data for all class methods
        # create a user object
        User.objects.create(username='default', password='password', email='email@gmail.com')

    def setUp(self) -> None:
        # Runs once for every test method to set up clean data
        return super().setUp()
    
    def testusernamelabel(self):
        user = User.objects.get(id=1)
        label = user._meta.get_field('username').verbose_name
        self.assertEqual(label, 'username')
