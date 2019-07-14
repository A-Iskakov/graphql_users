from faker import Faker
from graphene_django.utils import GraphQLTestCase
from ujson import loads

from api_endpoint.models import User
from graphql_users import schema


def create_initial_fake_data():
    fake = Faker('ru_RU')
    User.objects.bulk_create([User(first_name=fake.first_name(),
                                   username=fake.safe_email(),
                                   last_name=fake.last_name(),
                                   email=fake.safe_email(),
                                   )
                              for _ in range(50)], ignore_conflicts=True)


class UsersTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        create_initial_fake_data()

    def test_query(self):
        response = self.query(
            '''
            query {  
              users(firstName_Icontains: "а")
              {
                edges
                {
                  node
                  {
                      id
                      firstName          
                      email         
                      lastName
                      dateJoined
                      lastLogin         
                  }
                }
              }  
            }
            ''',
            op_name='users'
        )
        # print(response.content)
        content = loads(response.content)
        # print(content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertIsInstance(content['data']['users']['edges'], list)

        # Add some more asserts if you like
        ...

    def test_create_mutation(self):
        response = self.query(
            '''
            mutation{
              createUser(email: "aa@s3.dz" password: "asdfds1234" username: "2a331231",
                            firstName: "Azamat", lastName: "Iskakov")
              {
                newUser{id
                      firstName                      
                      email                    
                      lastName
                      dateJoined
                      lastLogin
                     
                    
               
                  }
                }
              }
            ''',
            op_name='createUser',

        )
        content = loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createUser']['newUser'][0]['id'], '51')

    def test_update_mutation(self):
        response = self.query(
            '''
            mutation{
              updateUser(id: 18 email: "a221112a@s3.jhz" password: "asdf111ds1234" username: "asdsd",
                            firstName: "aaAzamat", lastName: "Iaaskakov")
              {
                updatedUser{
                
                 
                  
                             id
                      firstName
                      # password
                      email
                      # isSuperuser
                      lastName
                      dateJoined
                      lastLogin
                      # username
                      # isStaff
                      # isActive
                    
               
                  }
                }
              }
            ''',
            op_name='updateUser',

        )
        content = loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateUser']['updatedUser'][0]['id'], '18')
