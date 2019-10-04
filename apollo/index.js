const { ApolloServer, ApolloError } = require('apollo-server');
const gql = require('graphql-tag');
const {getData, postData} = require('./helpers');
const { print } = require('graphql');

const typeDefs = gql`

  type DevExplore {
    result: OneToFive!
  }

  type RoleID {
    role_id: Int!
  }

  enum OneToFive {
    One
    Two
    Three
    Four
    Five
  }

  type AssetID {
    asset_id: Int!
  }
    
  type AssetRoleID {
    asset_id: Int!
    role_id: Int!
  }

  type Result {
    affected_rows: Int!
  }

  type Query {
    dev_explore(result: Boolean!): DevExplore
  }

  input MissingRole {
    role_number: String!
    role_name: String!
    role_criticality: Int
    role_priority: Int
    role_spatial_site_id: Int
    parent: Int!
  }

  input MissingAsset {
    asset_serial_number: String!
  }

  input id_eq {
    _eq: Int!
  }

  input where_id {
    id: id_eq!
  }

  input set {
    role_id: Int
    entity_exists: Boolean
    parent: Int
    asset_id: Int
  }

  input set_role {
    role_id: Int
  }

  type Mutation {
    insert_reconciliation_view(objects: MissingRole!): Result
    insert_unassigned_assets(objects: MissingAsset!): Result
    update_unassigned_assets(where: where_id!, _set: set_role!): Result
    update_reconciliation_view(where: where_id!, _set: set!): Result
    delete_unassigned_assets(where: where_id!): Result
    dev_add_explore(where: OneToFive): Result
  }

`;
//const djangoAPIENDpoint = 'http://django.tw-webapp.duckdns.org/api';
//const djangoAPIENDpoint = 'http://tw-webapp.duckdns.org/api';
const djangoAPIENDpoint = 'http://localhost:8000/api';

const resolvers = {
  // dummy query not actually used for anything
  Query: {
    dev_explore: async (_, { result }) => {
        var nameParams = '';
        if (result) {
            nameParams = '?name=' + result;
        }
        return await getData(restAPIEndpoint + '/fail/');
    }
  },
  Mutation: {
    insert_reconciliation_view: async (_, { objects } ) => {
      // remove defaults and change to mandatory value after demo
      var role_number = objects.role_number
      var parent_id = objects.parent
      var role_criticality = (typeof objects.role_criticality === 'undefined') ? 1 : objects.role_criticality
      var role_name = objects.role_name
      var role_priority = (typeof objects.role_priority === 'undefined') ? 1 : objects.role_priority
      var role_spatial_site_id = (typeof objects.role_spatial_site_id === 'undefined') ? 1 : objects.role_spatial_site_id
      return await postData(djangoAPIENDpoint + '/missing-role/', { role_number, role_spatial_site_id, role_priority, role_name, role_criticality, parent_id });
    },
    insert_unassigned_assets: async (_, { objects } ) => {
      var asset_serial_number = objects.asset_serial_number
      return await postData(djangoAPIENDpoint + '/missing-asset/', { asset_serial_number });
    },
    update_unassigned_assets: async (_, { where, _set } ) => {
      var asset_id = where.id._eq
      var role_id = _set.role_id
      return await postData(djangoAPIENDpoint + '/assign-asset-to-role/', { asset_id, role_id });
    },
    update_reconciliation_view: async (_, { where, _set } ) => {
      // assigning asset to new role w: asset id, s:role id
      // does not exist w: role id, s: does not exist = false
      if (_set.role_id !== undefined) { //this might not be getting used
        var asset_id = where.id._eq
        var role_id = _set.role_id
        return await postData(djangoAPIENDpoint + '/assign-asset-to-role/', { asset_id, role_id });
      } else if (_set.entity_exists !== undefined) {
        var role_id = where.id._eq
        var entity_exists = _set.entity_exists
        return await postData(djangoAPIENDpoint + '/entity-exists/', { entity_exists, role_id });
      } else if (_set.parent !== undefined) {
        var role_id = where.id._eq
        var parent_id = _set.parent
        return await postData(djangoAPIENDpoint + '/set-role-parent/', { parent_id, role_id });
      } else if (_set.asset_id !== undefined) {
        var role_id = where.id._eq
        var asset_id = _set.asset_id
        return await postData(djangoAPIENDpoint + '/assign-asset-to-role/', { asset_id, role_id });
      } 
    },
    delete_unassigned_assets: async (_, { where } ) => {
      var asset_id = where.id._eq
      return await postData(djangoAPIENDpoint + '/retire-asset/', { asset_id });
    },
    dev_add_explore: async (_, { where } ) => {
      return await postData(djangoAPIENDpoint + '/dev-explore/', { where });
    },
  }
};
//
class BasicLogging {
  requestDidStart({queryString, parsedQuery, variables}) {
    const query = queryString || print(parsedQuery);
    console.log(query);
    console.log(variables);
  }

  willSendResponse({graphqlResponse}) {
    console.log(JSON.stringify(graphqlResponse, null, 2));
  }
}

const schema = new ApolloServer({ 
  typeDefs,
  resolvers,
  introspection: true,
  playground: true,
  extensions: [() => new BasicLogging()]
});

schema.listen({ port: process.env.PORT || 4000 }).then(({ url }) => {
    console.log(`schema ready at ${url}`);
});

// logging per https://stackoverflow.com/questions/54273194/log-apollo-server-graphql-query-and-variables-per-request