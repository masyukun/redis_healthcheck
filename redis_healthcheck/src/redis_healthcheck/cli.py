import json
import pkg_resources
import re
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich import print

import click



# Resource stuff
pluginSiteUrl = "https://TBD/"
console = Console()
SERVER_LIST = 'serverList.json'
PLUGIN_ORDER = ['collect','detect','correct']
CSV_CHECKS_FILENAME = 'check-report-{}.csv'.format(datetime.now().strftime("%Y-%d-%m-%H%M%S"))

# The Context -- I feel conflicted using this # https://wiki.c2.com/?ContextObjectsAreEvil
context = {}
noCodeChecks = {}



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


def openCheckFile(ctx, param, filenames):
    """Use a JSON checkfile to drive constraint checking"""

    checkfileSpecs = []

    # Handle one or more filenames
    fns = []
    if (type(filenames) == type([]) or type(filenames) == type(())):
      fns.extend(filenames)
    else:
      print(type(filenames))
      fns.append(filenames)

    for filename in filenames:
      _stream = open(filename)
      _dict = json.load(_stream)
      _stream.close()
      checkfileSpecs.append({"filename": filename, "checks": _dict})
         
    # print('DEBUG CHECKFILES = {}'.format(checkfileSpecs))
    return checkfileSpecs


# Recursively descend the library Dict to find the fieldname and check the constraint
def checkConstraint(library, fieldname, constraint, value):
  thepath = None
  thevalue = None
  fitsConstraint = None
  
  # print('ENTERED checkConstraint')
  # print(library)

  # Terminal condition
  if fieldname in library:
    # NOTE: Not using match case statement for greater Pythonic compatibility
    if constraint.lower() in ["==","=","eq"]:
      return [fieldname], library[fieldname], library[fieldname] == value
    elif constraint.lower() in [">=",">==","ge"]:
      return [fieldname], library[fieldname], library[fieldname] >= value
    elif constraint.lower() in ["<=","<==","le"]:
      return [fieldname], library[fieldname], library[fieldname] <= value
    elif constraint.lower() in [">","lt"]:
      return [fieldname], library[fieldname], library[fieldname] > value
    elif constraint.lower() in ["<","gt"]:
      return [fieldname], library[fieldname], library[fieldname] < value
    elif constraint.lower() in ["!=","<>","ne"]:
      return [fieldname], library[fieldname], library[fieldname] != value
    else:
      raise Exception('Unsupported operator: {}'.format(constraint))
  else:

    # Recurse down the remaining arrays/tuples and objects
    for k in library.keys():

      if type(library[k]) == type({}):
        # print('-->Descending "{}" type {}'.format(k, type(library[k])))
        thepath, thevalue, fitsConstraint = checkConstraint(library[k], fieldname, constraint, value)
        # print('fitsConstraint = {}'.format(fitsConstraint))
        
        # If there was a result down there, pass it on
        if fitsConstraint is not None:
          # Reconstruct the path, bottom up
          thepath.insert(0, k)
          # print('  breaking!')
          break
      elif type(library[k]) == type([]) or type(library[k]) == type(()):
        for i, item in enumerate(library[k]):
          if type(item) == type({}):
            # print('-->Descending "{}"[{}]'.format(k, i))
            thepath, thevalue, fitsConstraint = checkConstraint(item, fieldname, constraint, value)
            # print('fitsConstraint = {}'.format(fitsConstraint))

            # If there was a result down there, pass it on
            if fitsConstraint is not None:
              # Reconstruct the path, bottom up
              thepath.insert(0, "{}[{}]".format(k, i))
              # print('  breaking!')
              break
        # If there was a result down there, pass it on
        if fitsConstraint is not None:
          # print('  breaking!')
          break

      # else:
      #   print('Skipping "{}" type {}'.format(k, type(library[k])))

  # print('Returning result = {}'.format(result))
  return thepath, thevalue, fitsConstraint


@click.group()
@click.option('-s', '--serverList', type=click.Path(dir_okay=False), default=SERVER_LIST, help='JSON containing list of servers [{fqdn, username, password},{...},...] of each managed Redis Enterprise cluster.', multiple=False, callback=openServerList)
@click.option('-c', '--checkfile', type=click.Path(dir_okay=False), required=False, help='JSON containing constraints to check against the configuration.', multiple=True, callback=openCheckFile)
@click.pass_context
def cli(ctx, serverlist, checkfile):
  """Redis Enterprise Healthcheck Tool"""
  context["serverList"] = serverlist
  noCodeChecks["checkfile"] = checkfile
  ctx.obj = context


@cli.command()
@click.option('-o', '--output', default=CSV_CHECKS_FILENAME, help='Filename for check report as CSV', multiple=False, required=False, show_default=True)
@click.pass_obj
def start(context, output):
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

        # TODO Make this less dangerous... provide a READONLY view of the context
        print('\nRunning plugin "{}"...'.format( plugin['name'] ))
        result = plugin['metadata'][pluginType](context)

        # Save the result back as context
        # TODO Make this less dangerous... in case plugins don't return the context
        if result is not None:
          context = result

  # print('DEBUG CONTEXT = {}'.format(context))

  # Run the Checkfiles
  if noCodeChecks["checkfile"] is not None:
    # csv = "Constraint source,Constraint field name,Constraint,Constraint value,Observed value,Passed"
    structuredChecks = []
    checkResults = []

    # Read each checkfile, process each checkfile format
    print("\n:clipboard: {} checkfile{} found".format(len(noCodeChecks["checkfile"]), "s" if len(noCodeChecks["checkfile"]) != 1 else ""))
    for checkfile in noCodeChecks["checkfile"]:
      print('  Processing checkfile "{}"...'.format(checkfile['filename']))
      for checkname in checkfile['checks'].keys():
        check = checkfile['checks'][checkname]
        if 'constraint' in check:
          structuredChecks.append({'checkfile': checkfile['filename'],'checkfield':checkname,'constraint':check['constraint'],'error':check['error'],'value':check['value'],'message':check['message']})
        else:
          # TODO
          print('    "{}" <-- String constraint not yet implemented'.format(checkname))
    
    # Do the checks and store the results
    print("\n:clipboard: Running checks...")
    for check in structuredChecks:
      check['checkResult'] = {}
      check['checkResult']['path'], check['checkResult']['actualValue'], check['checkResult']['matchesConstraint'] = checkConstraint(context, check['checkfield'], check['constraint'], check['value'])
      
      # DEBUG screen output
      print('"{}" {} {}'.format(check['checkfield'], check['constraint'], check['value']))
      print('  {}'.format(":white_check_mark: matches at {}".format("/".join(check['checkResult']['path'])) if check['checkResult']['matchesConstraint'] 
        else ":warning: field not found" if check['checkResult']['matchesConstraint'] is None 
        else ":x: constraint failed; saw = {} but expected {} {} at {}".format(check['checkResult']['actualValue'], check['constraint'], check['value'], "/".join(check['checkResult']['path']))))

      checkResults.append(check)
    
    # Output the results of the checks to a report file
    print('\n:clipboard: Writing CSV report file to "{}"'.format(output))
    csv = "Constraint source,Constraint field name,Constraint,Constraint value,Observed value,Passed"
    for check in checkResults:
      csv += '\n{},{},{},{},{},{}'.format(
        check['checkfile'],
        check['checkfield'], check['constraint'], check['value'],
        check['checkResult']['actualValue'], check['checkResult']['matchesConstraint']
      )
    reportOutput = open(output, "w")
    reportOutput.write(csv)
    reportOutput.close()

  else:
    print("\n:no_entry_sign: No checkfiles specified")



# Only run main when run as CLI
if __name__ == "__main__":
  cli()
