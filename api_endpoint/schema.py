from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.db import IntegrityError
from graphene import relay, Mutation, String, ID
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from api_endpoint.models import User

SEARCH_FILTERS = ['exact', 'icontains', 'istartswith']


class DjangoNode(relay.Node):
    """
    This class removes base64 unique ids and operates with plain Integer ID
    """

    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        node = super().get_node_from_global_id(info, global_id, only_type)
        if node:
            return node

        get_node = getattr(only_type, 'get_node', None)
        if get_node:
            return get_node(info, global_id)

    @classmethod
    def to_global_id(cls, type, id):
        return id


class UserNode(DjangoObjectType):
    """
        This class gives a representation of a User model
        """

    class Meta:
        model = User

        # exclude django admin specific information
        exclude_fields = ("is_superuser", "is_staff", "password", 'username',)

        filter_fields = {
            'first_name': SEARCH_FILTERS,
            'last_name': SEARCH_FILTERS,
            'email': SEARCH_FILTERS,
            'id': ['exact'],

        }

        interfaces = (DjangoNode,)


class ApiQuery(object):
    """
        This class queries all users except django super users
        """

    users = DjangoFilterConnectionField(UserNode)

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(is_superuser=False)


class UserCreateMutation(Mutation):
    """
           This class creates new users
           """

    class Arguments:
        # The input arguments for this mutation
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        first_name = String()
        last_name = String()

    new_user = DjangoListField(UserNode)

    def mutate(self, info, username, email, password, first_name, last_name):

        # validate input information first
        try:
            validate_email(email)
            validate_password(password)
            user = User.objects.create_user(username, email, password,
                                            first_name=first_name,
                                            last_name=last_name)
        except (ValidationError, IntegrityError) as message:
            raise GraphQLError(str(message))
        else:
            # if ok return new user
            return UserCreateMutation(new_user=[user])


class UserUpdateMutation(Mutation):
    """
              This class updates exciting users
              """

    class Arguments:
        # The input arguments for this mutation
        id = ID(required=True)

        email = String()
        password = String()
        username = String()
        first_name = String()
        last_name = String()

    updated_user = DjangoListField(UserNode)

    def mutate(self, info, id, email, password, **kwargs):
        try:
            # get a user which is not a superadmin
            user = User.objects.get(id=id, is_superuser=False)

            # check pass
            if password:
                validate_password(password)
                user.set_password(password)

            # check email
            if email:
                validate_email(email)
                user.email = email

            # set other user kwargs
            for key, value in kwargs.items():
                setattr(user, key, value)

            # save
            user.save()
        except (ValidationError, IntegrityError, ObjectDoesNotExist) as message:
            raise GraphQLError(str(message))
        else:
            return UserUpdateMutation(updated_user=[user])


class ApiMutation(object):
    create_user = UserCreateMutation.Field()
    update_user = UserUpdateMutation.Field()
