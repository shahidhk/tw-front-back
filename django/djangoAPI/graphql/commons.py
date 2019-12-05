import graphene
import requests
from django.db import models
# classes for inputs


class EQ(graphene.InputObjectType):
    _eq = graphene.Int(required=True)


class IDEQ(graphene.InputObjectType):
    id = EQ(required=True)
    asset_id = EQ(required=True)


class TableType(graphene.ObjectType):
    name = graphene.String()
    query_type = graphene.String()


class QueryTypeCache(models.Model):
    """
    Model to cache the type of queries
    """
    name = models.CharField(max_length=100, unique=True)
    query_type = models.TextField()

    @staticmethod
    def update(name):
        """
        if entry does not exist update the db
        """
        query = "{ __schema { queryType { name description fields { name type { kind name ofType { name kind ofType { ofType { name } } } } } } } } "
        response = requests.post(
            'https://hasura.tw-webapp-next.duckdns.org/v1/graphql',
            json={'query': query},
            headers={'x-hasura-admin-secret': 'eDfGfj041tHBYkX9'}
        )
        for field in response.json()['data']['__schema']['queryType']['fields']:
            if not field['type']['ofType']:
                continue
            elif field['type']['ofType']['kind'] == 'OBJECT':
                query_type = field['type']['ofType']['name']
            elif field['type']['ofType']['kind'] == 'LIST':
                query_type = field['type']['ofType']['ofType']['ofType']['name']
            else:
                print('undefined type for %s' % (field['name']))
            temp = QueryTypeCache.objects.update_or_create(
                name=field['name'],
                query_type=query_type,
            )
            if field['name'] == name:
                result = temp
        return result[0]
