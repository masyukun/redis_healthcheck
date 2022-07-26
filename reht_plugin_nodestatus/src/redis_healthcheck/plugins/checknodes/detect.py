from rich.console import Console
from rich.table import Table
from rich import print



requiredFields = ['serverList']


def plugin_metadata():
    # Return a standard plugin metadata object to the framework
    return {
        "description": "This plugin checks the nodes status.",
        "type": "detect",
        "requiredFields": requiredFields,

        # Entry points
        "detect": detect,
    }


def detect(context):
  """Run the node check status job. Requires the context containing server configuration object as a dict."""

  # Sanity test that we have the required incoming context data
  if context is None:
    raise ValueError("This plugin requires a context object as a parameter.")

  for requiredField in requiredFields:
    if requiredField not in context:
      raise ValueError("The context is missing a required field: \"{}\"".format(requiredField))


  # Get more sanity on whether there are nodes in the configuration object
  for server in context['serverList']:
    print('Cluster "{}" ...'.format(server['fqdn']))
    if 'configurations' not in server:
      print('  :ghost: Skipping cluster because there is no configuration object. Try again after running plugin "collector_configuration".')
      continue
    if 'nodes' not in server['configurations']:
      print('  :ghost: Skipping cluster because there are no nodes listed in the configuration object.".')
      continue
    

    # Build table
    console = Console()
    nodeTable = Table(show_header=True, header_style="bold blue")
    nodeTable.add_column("Address")
    nodeTable.add_column("OS Version")
    nodeTable.add_column("Shards")
    nodeTable.add_column("Status")
    for node in server['configurations']['nodes']:
      
      # Fill the table with plugin data
      nodeTable.add_row(
        node['addr'],
        node['os_version'],
        ", ".join( [str(n) for n in node['shard_list']] ),
        node['status'] if node['status'] == 'active' else '[bold red]{}[/bold red]'.format(node['status']),
      )
  
    # Show the table
    console.print(nodeTable)



  # Return a data object
  return context




def main():
  print("Sorry, but this package cannot be run on the command line.")
  print("Please run it from the Redis Healthcheck Tool. pip3 install redis_healthcheck")


# Only run main when run as CLI
if __name__ == "__main__":
  main()


# SAMPLE NODE OBJECT
# 
# {
#     'accept_servers': True,
#     'addr': '172.17.0.2',
#     'architecture': 'x86_64',
#     'bigredis_storage_path': '/var/opt/redislabs/flash',
#     'bigstore_driver': '',
#     'cores': 4,
#     'ephemeral_storage_path': '/var/opt/redislabs/tmp',
#     'ephemeral_storage_size': 63089455104.0,
#     'external_addr': [],
#     'max_listeners': 100,
#     'max_redis_servers': 100,
#     'os_name': 'ubuntu',
#     'os_semantic_version': '18.04',
#     'os_version': 'Ubuntu 18.04.6 LTS',
#     'persistent_storage_path': '/var/opt/redislabs/persist',
#     'persistent_storage_size': 63089455104.0,
#     'rack_id': '',
#     'shard_count': 1,
#     'shard_list': [2],
#     'software_version': '6.2.10-121',
#     'status': 'active',
#     'supported_database_versions': [
#         {'db_type': 'redis', 'version': '6.2.5'},
#         {'db_type': 'memcached', 'version': '1.4.17'},
#         {'db_type': 'redis', 'version': '6.0.13'}
#     ],
#     'total_memory': 4127694848,
#     'uid': 1,
#     'uptime': 28654
# }
