import pkg_resources

# query all of the console_scripts that are installed in your Python environment
for ep in pkg_resources.iter_entry_points(group='console_scripts'):
  print("{name} = {module_name}{attrs}".format(\
      name=ep.name,
      module_name=ep.module_name,
      attrs=ep.attrs))
