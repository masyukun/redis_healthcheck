import json
import pkg_resources
import re

from rich.console import Console
from rich.table import Table
from rich import print

import click



# Resource stuff
pluginSiteUrl = "https://TBD/"
console = Console()
SERVER_LIST = 'serverList.json'
PLUGIN_ORDER = ['collect','detect','correct']

# The Context -- I feel conflicted using this # https://wiki.c2.com/?ContextObjectsAreEvil
context = {}



def getPlugins():
  """Query this Python environment's pkg_resources 
  for any installed Redis Healthcheck plugins. 
  Returns a list of them to the calling function."""

  pluginList = []

  # Query for healthcheck plugins installed in this Python environment
  for ep in pkg_resources.iter_entry_points(group='redis_healthcheck_plugin'):

    pluginList.append({
      'entrypoint': ep.load(),
      'name': ep.name,
      'module_name': ep.module_name,
      'attrs': ep.attrs,
      'dist': ep.dist,
      'extras': ep.extras,
    })

    # # Run the plugin
    # pluginCode = ep.load()
    # pluginCode()

  # Sort plugins alphabetically
  pluginList = sorted(pluginList, key=lambda d: d['name']) 

  # List the plugins
  if len(pluginList) > 0:
    print(" :electric_plug: I'm seeing {num} plugin{s} on this system:".format(
      num=len(pluginList), 
      s=("" if len(pluginList) == 1 else "s")
      )
    )

    # Build table
    pluginTable = Table(show_header=True, header_style="bold magenta")
    pluginTable.add_column("Version", style="dim", width=12)
    pluginTable.add_column("Plugin Name")
    pluginTable.add_column("Project Name")
    
    # Fill the table with plugin data
    for p in pluginList:
      pluginTable.add_row(
        p['dist'].version,
        p['name'],
        p['dist'].project_name,
      )
    
    # Show the table
    console.print(pluginTable)

  else:
    # No plugins
    print(" :electric_plug: Doesn't look like you have any plugins.")
    print(" :snake: You can install them with pip. (Plugin list: {pluginSite})".format(pluginSite=pluginSiteUrl))

  
  return pluginList


def validate_fqdn(fqdn):
    """Validate and sanitize the incoming FQDN server"""
    
    # Sanitize incoming FQDN
    print('\n')
    fqdn = fqdn.strip()
    if re.match(r'^.*?://', fqdn):
        # print('Trimming protocol handler in FQDN...')
        fqdn = re.split(r'^.*?://', fqdn)[-1]
        fqdn = "https://" + fqdn
    if fqdn[-1] == '/':
        # print('Trimming trailing slash in FQDN...')
        fqdn = fqdn[0:-1]
    return fqdn


def openServerList(ctx, param, filename):
    """Open the specified JSON file and use as the server list"""

    _stream = open(filename)
    _dict = json.load(_stream)
    _stream.close()

    # Normalize incoming FQDNs for downstream use
    for server in _dict:
      if 'fqdn' in server:
        server['fqdn'] = validate_fqdn(server['fqdn'])
      else:
        print('No FQDN found in server = {}'.format(server))

    return _dict


@click.group()
@click.option('-s', '--serverList', type=click.Path(dir_okay=False), default=SERVER_LIST, help='JSON containing list of servers [{fqdn, username, password},{...},...] of each managed Redis Enterprise cluster.', multiple=False, callback=openServerList)
@click.pass_context
def cli(ctx, serverlist):
  """Redis Enterprise Healthcheck Tool"""
  context["serverList"] = serverlist
  ctx.obj = context


@cli.command()
@click.pass_obj
def start(context):
  """Run Redis Healthcheck from CLI."""

  print(" :hospital: Oh hey! Let's do a Redis Healthcheck.")

  # List the plugins
  pluginList = getPlugins()

  # print("Let's navigate the plugin list structure :smile:")
  # print(pluginList)

  # Load the plugins
  for plugin in pluginList:
    print("Loading plugin ""{}""...".format( plugin['name'] ))
    
    # Get the plugin metadata and entrypoints
    plugin['metadata'] = plugin['entrypoint']()

    # Sanity check
    if plugin['metadata'] is None:
      print(" :crossmark: This plugin has no metadata and thus no entrypoint.")


  # Run the plugins, in order.
  if len(pluginList) > 0:
    for pluginType in PLUGIN_ORDER:
      print('\nRunning plugin type "{}"'.format(pluginType))
      for plugin in [p for p in pluginList if "metadata" in p and pluginType in p["metadata"]['type']]:
        print('\nRunning plugin "{}"...'.format( plugin['name'] ))
        result = plugin['metadata'][pluginType](context)
        # print(result)




# Only run main when run as CLI
if __name__ == "__main__":
  cli()
