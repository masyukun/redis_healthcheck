import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from rich import print

# Suppress warnings over self-signed certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


requiredFields = ['serverList']


def plugin_metadata():
    # Return a standard plugin metadata object to the framework
    return {
        "description": "This plugin collects configuration data from a Redis Enterprise cluster and returns it as an object.",
        "type": "collect",
        "requiredFields": requiredFields,

        # Entry points
        "collect": collect,
    }


def sanitize(reference, dirtyObject):
    """Using the reference of Configuration Items (CIs), 
    sanitize the incoming dirtyObject
    and return a new sanitized object containing only keys from the reference object."""

    sanitizedObject = {}

    for k in reference:
        sanitizedObject[k] = dirtyObject[k] if k in dirtyObject else None

    return sanitizedObject


def buildConfigurationObject(server, cluster, ldap, ldap_mappings, roles, redis_acls, users, nodes, bdbs):
    """Package server configuration responses into a Configuration Object. 
    Removes all elements except configuration items."""

    configObject = {
        "cluster": cluster,
        "ldap": ldap,
        "ldap_mappings": [] + ldap_mappings,
        "roles": [] + roles,
        "redis_acls": [] + redis_acls,
        "users": [] + users,
        "nodes": [] + nodes,
        "bdbs": [] + bdbs
    }

    return configObject


def getReqJson(server, url):
    """Make a GET request to the server and unwrap its JSON"""
    # print('URL = {}'.format(url))
    json = None

    # Make the request
    response = requests.get(url, auth=HTTPBasicAuth(server['username'], server['password']), verify=server['accept_secure_certs_only'])

    # Parse and handle errors
    if (response.status_code == 200):
        try: json = response.json()
        except: print('Server [{}] did not return a JSON object'.format(url))
    else:
        if (response is not None): print("Request to [{}] responded with {} ".format(url, response.status_code))
    
    return json


def getServerConfiguration(server):
    """Contact 8 REST API endpoints for the server's current configuration."""

    # print("\nContacting server: {}".format(server['fqdn']))
    
    # GET /v1/cluster # Retrieve cluster information
    cluster = getReqJson(server, '{}/v1/cluster'.format(server['fqdn']))

    # GET /v1/cluster/ldap # Get the LDAP configuration
    ldap = getReqJson(server, '{}/v1/cluster/ldap'.format(server['fqdn']))

    # GET /v1/ldap_mappings # Get all the LDAP mapping objects
    ldap_mappings = getReqJson(server, '{}/v1/ldap_mappings'.format(server['fqdn']))

    # GET /v1/roles # Get all role objects
    roles = getReqJson(server, '{}/v1/roles'.format(server['fqdn']))

    # GET /v1/redis_acls # Get the list of all ACLs in the cluster
    redis_acls = getReqJson(server, '{}/v1/redis_acls'.format(server['fqdn']))

    # GET /v1/users # Get all RLEC users
    users = getReqJson(server, '{}/v1/users'.format(server['fqdn']))

    # GET /v1/nodes # Retrieve a list of nodes
    nodes = getReqJson(server, '{}/v1/nodes'.format(server['fqdn']))

    # GET /v1/bdbs # Get all databases
    bdbs = getReqJson(server, '{}/v1/bdbs'.format(server['fqdn']))


    # Print data got
    print('Cluster received %s elements' % (len(cluster) if cluster is not None else 0) )
    print('LDAP received %s elements' % (len(ldap) if ldap is not None else 0) )
    print('ldap_mappings received %s elements' % (len(ldap_mappings) if ldap_mappings is not None else 0) )
    print('roles received %s elements' % (len(roles) if roles is not None else 0) )
    print('redis_acls received %s elements' % (len(redis_acls) if redis_acls is not None else 0) )
    print('users received %s elements' % (len(users) if users is not None else 0) )
    print('nodes received %s elements' % (len(nodes) if nodes is not None else 0) )
    print('bdbs received %s elements' % (len(bdbs) if bdbs is not None else 0) )


    # Package server responses into a trackable object
    config = buildConfigurationObject(server, cluster, ldap, ldap_mappings, roles, redis_acls, users, nodes, bdbs)


    return config


def collect(context):
  """Run the configuration collector plugin code. Requires the context containing server connection information as a dict."""

  # Sanity test that we have the required incoming context data
  if context is None:
    raise ValueError("This plugin requires a context object as a parameter.")

  for requiredField in requiredFields:
    if requiredField not in context:
      raise ValueError("The context is missing a required field: \"{}\"".format(requiredField))


  # Get configuration for each server in the list
  for server in context['serverList']:
    print('Calling getServerConfiguration for server {} ...'.format(server['fqdn']))
    try:
      server['configurations'] = getServerConfiguration(server)
      print(' :book: Success! Retrieved configuration object from REST API.\n')
    except ConnectionError:
      print(' :skull: Failed connecting to server "{}"...'.format(server['fqdn']))



  # Return a data object
  return context




def main():
  print("Sorry, but this package cannot be run on the command line.")
  print("Please run it from the Redis Healthcheck Tool. pip3 install redis_healthcheck")


# Only run main when run as CLI
if __name__ == "__main__":
  main()
