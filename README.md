# redis_healthcheck
Redis Enterprise Healthcheck Tool with plugin framework. This project is intended to be a Swiss Army Knife style tool for quickly diagnosing common problems in Redis Enterprise clusters.



# Setting up your Python environment

First, set up your environment for this project, so that it's separate from your main `python3` environment. 

```console
~/GitHub$ cd redis_healthcheck/
~/GitHub/redis_healthcheck$ python3 -m virtualenv -p python3 venv
```

```console
created virtual environment CPython3.7.9.final.0-64 in 719ms
  creator CPython3Posix(dest=/Users/matthewroyal/Documents/GitHub/redis_healthcheck/venv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/Users/matthewroyal/Library/Application Support/virtualenv)
    added seed packages: pip==22.1.2, setuptools==62.6.0, wheel==0.37.1
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
```

```console
~/GitHub/redis_healthcheck$ source ./venv/bin/activate

(venv) ~/GitHub/redis_healthcheck$ 
```

From here on out, any packages you install with `pip` are specific to this Python project. You can tell that you're in a `venv` virtual environment thanks to the `(venv)` prefix on your command shell.

To leave the `venv` session, type `deactivate`:

```console
(venv) ~/GitHub/redis_healthcheck$ deactivate

~/GitHub/redis_healthcheck$ 
```

For the rest of this README, we will assume you are in the environment of your choice, so further console prompts will not necessarily show the `(venv)` prefix.



# Installation from source

Assuming you have Python 3 installed, you can install everything using the `pip` command either directly from the source <span style="color:red">or (TBD) from the public PyPi repo</span>. 

`pip` can build packages from local source files, and *that is the current recommended method of installation during the initial development phase*.

Basically, you point `pip` at the source folder you want it to build with the `-e` flag. The projects are already structured in a way that `pip` knows how to read and generate a package. It will read the source, build an egg package, and install it into your environment. Installation will also install any required `pip` packages, which it will download from the Internet if they're not already installed in your environment. After that, you can use the name of the package itself to run the code.

```console
~/GitHub/redis_healthcheck$ pip install -U -e redis_healthcheck
```

```console
Obtaining file:///Users/matthewroyal/Documents/GitHub/redis_healthcheck/redis_healthcheck
  Preparing metadata (setup.py) ... done
Collecting future
  Using cached future-0.18.2-py3-none-any.whl
Collecting rich
  Using cached rich-12.5.1-py3-none-any.whl (235 kB)
Collecting click
  Using cached click-8.1.3-py3-none-any.whl (96 kB)
Collecting importlib-metadata
  Using cached importlib_metadata-4.12.0-py3-none-any.whl (21 kB)
Collecting typing-extensions<5.0,>=4.0.0
  Using cached typing_extensions-4.3.0-py3-none-any.whl (25 kB)
Collecting pygments<3.0.0,>=2.6.0
  Using cached Pygments-2.12.0-py3-none-any.whl (1.1 MB)
Collecting commonmark<0.10.0,>=0.9.0
  Using cached commonmark-0.9.1-py2.py3-none-any.whl (51 kB)
Collecting zipp>=0.5
  Using cached zipp-3.8.1-py3-none-any.whl (5.6 kB)
Installing collected packages: commonmark, zipp, typing-extensions, pygments, future, rich, importlib-metadata, click, redis-healthcheck
  Running setup.py develop for redis-healthcheck
Successfully installed click-8.1.3 commonmark-0.9.1 future-0.18.2 importlib-metadata-4.12.0 pygments-2.12.0 redis-healthcheck-0.0.1 rich-12.5.1 typing-extensions-4.3.0 zipp-3.8.1
```


## Server List

The `redis_healthcheck` command needs to know where to perform the healthcheck, and for that we use the `serverList.json` file <span style="color:red">or (TBD)specify the server using an application flag --server<server></span>. You should create a file called `serverList.json` in the same directory you run the `redis_healthcheck` command in.

Here's a sample `serverList.json` file:

```json
[
  {
    "fqdn": "https://localhost:9443/",
    "username": "admin@rl.org",
    "password": "imtheadmin",
    "accept_secure_certs_only": false
  }
]
```

You can specify any number of Redis Enterprise clusters here.
 * `fqdn` - This field is the same type of string you'd use in connecting cluster nodes together -- this should be an address that is reachable on the network, and it must point to the REST API interface port 9443.
 * `username` - This user must have at least "cluster viewer" privileges on the machine. Admin privileges work here too, but may be excessive.
 * `password` - The password for this user
 * `accept_secure_certs_only` - If you are using a self-signed cert or the certificate is otherwise not in your local machine's trust store, you can ignore good security practices and force a connection to the server with the `false` value.


## Installing plugins

Installing plugins with `pip` is just like installing the base application. Plugins come in a few flavors:
* `collectors` - These provide data to the healthcheck system, such as cluster configuration data or metrics.
* `detectors` - These diagnose issues or generate reports on the system.
* `correctors` - These are bundled with some `detectors` and can (optionally) correct detected issues, when possible.

### Installing plugins: collector_configuration

To install the `configuration-collector` plugin, make sure you're in the base project directory and run:

```console
~/GitHub/redis_healthcheck$ pip install -U -e reht_plugin_configuration
```

```console
Obtaining file:///Users/matthewroyal/Documents/GitHub/redis_healthcheck/reht_plugin_configuration
  Preparing metadata (setup.py) ... done
Requirement already satisfied: future in ./venv/lib/python3.7/site-packages (from RE-Healthcheck-Plugin-Configuration-Collector==0.0.1) (0.18.2)
Collecting requests
  Using cached requests-2.28.1-py3-none-any.whl (62 kB)
Requirement already satisfied: rich in ./venv/lib/python3.7/site-packages (from RE-Healthcheck-Plugin-Configuration-Collector==0.0.1) (12.5.1)
Collecting certifi>=2017.4.17
  Using cached certifi-2022.6.15-py3-none-any.whl (160 kB)
Collecting charset-normalizer<3,>=2
  Using cached charset_normalizer-2.1.0-py3-none-any.whl (39 kB)
Collecting urllib3<1.27,>=1.21.1
  Using cached urllib3-1.26.11-py2.py3-none-any.whl (139 kB)
Collecting idna<4,>=2.5
  Using cached idna-3.3-py3-none-any.whl (61 kB)
Requirement already satisfied: pygments<3.0.0,>=2.6.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Configuration-Collector==0.0.1) (2.12.0)
Requirement already satisfied: commonmark<0.10.0,>=0.9.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Configuration-Collector==0.0.1) (0.9.1)
Requirement already satisfied: typing-extensions<5.0,>=4.0.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Configuration-Collector==0.0.1) (4.3.0)
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests, RE-Healthcheck-Plugin-Configuration-Collector
  Running setup.py develop for RE-Healthcheck-Plugin-Configuration-Collector
Successfully installed RE-Healthcheck-Plugin-Configuration-Collector-0.0.1 certifi-2022.6.15 charset-normalizer-2.1.0 idna-3.3 requests-2.28.1 urllib3-1.26.11
```

You can now run the healthcheck app using `redis_healthcheck start` and it will see the plugin you have installed:

```console
~/GitHub/redis_healthcheck$ redis_healthcheck start
```

```console


 🏥 Oh hey! Let's do a Redis Healthcheck.
 🔌 I'm seeing 1 plugin on this system:
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Version      ┃ Plugin Name             ┃ Project Name                                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0.0.1        │ collector_configuration │ RE-Healthcheck-Plugin-Configuration-Collector │
└──────────────┴─────────────────────────┴───────────────────────────────────────────────┘
Loading plugin collector_configuration...

Running plugin type "collect"

Running plugin "collector_configuration"...
Calling getServerConfiguration for server https://localhost:9443 ...
Cluster received 41 elements
LDAP received 12 elements
ldap_mappings received 0 elements
roles received 6 elements
redis_acls received 3 elements
users received 1 elements
nodes received 1 elements
bdbs received 1 elements
 📖 Success! Retrieved configuration object from REST API.


Running plugin type "detect"

Running plugin type "correct"

```

### Installing plugins: check_nodes

The Check Nodes plugin displays a table of all the nodes in a cluster, and highlights any that have a status other than `active` in red.

To install the `check_nodes` plugin, make sure you're in the base project directory and run:

```console
~/GitHub/redis_healthcheck$ pip install -U -e reht_plugin_nodestatus
```

```console
Obtaining file:///Users/matthewroyal/Documents/GitHub/redis_healthcheck/reht_plugin_nodestatus
  Preparing metadata (setup.py) ... done
Requirement already satisfied: future in ./venv/lib/python3.7/site-packages (from RE-Healthcheck-Plugin-Node-Status==0.0.1) (0.18.2)
Requirement already satisfied: requests in ./venv/lib/python3.7/site-packages (from RE-Healthcheck-Plugin-Node-Status==0.0.1) (2.28.1)
Requirement already satisfied: rich in ./venv/lib/python3.7/site-packages (from RE-Healthcheck-Plugin-Node-Status==0.0.1) (12.5.1)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in ./venv/lib/python3.7/site-packages (from requests->RE-Healthcheck-Plugin-Node-Status==0.0.1) (1.26.11)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.7/site-packages (from requests->RE-Healthcheck-Plugin-Node-Status==0.0.1) (3.3)
Requirement already satisfied: charset-normalizer<3,>=2 in ./venv/lib/python3.7/site-packages (from requests->RE-Healthcheck-Plugin-Node-Status==0.0.1) (2.1.0)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.7/site-packages (from requests->RE-Healthcheck-Plugin-Node-Status==0.0.1) (2022.6.15)
Requirement already satisfied: pygments<3.0.0,>=2.6.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Node-Status==0.0.1) (2.12.0)
Requirement already satisfied: commonmark<0.10.0,>=0.9.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Node-Status==0.0.1) (0.9.1)
Requirement already satisfied: typing-extensions<5.0,>=4.0.0 in ./venv/lib/python3.7/site-packages (from rich->RE-Healthcheck-Plugin-Node-Status==0.0.1) (4.3.0)
Installing collected packages: RE-Healthcheck-Plugin-Node-Status
  Running setup.py develop for RE-Healthcheck-Plugin-Node-Status
Successfully installed RE-Healthcheck-Plugin-Node-Status-0.0.1
```

You can now run the healthcheck app using `redis_healthcheck start` and it will see the plugin you have installed:

```console
~/GitHub/redis_healthcheck$ redis_healthcheck start
```

```console


 🏥 Oh hey! Let's do a Redis Healthcheck.
 🔌 I'm seeing 2 plugins on this system:
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Version      ┃ Plugin Name             ┃ Project Name                                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0.0.1        │ check_nodes             │ RE-Healthcheck-Plugin-Node-Status             │
│ 0.0.1        │ collector_configuration │ RE-Healthcheck-Plugin-Configuration-Collector │
└──────────────┴─────────────────────────┴───────────────────────────────────────────────┘
Loading plugin check_nodes...
Loading plugin collector_configuration...

Running plugin type "collect"

Running plugin "collector_configuration"...
Calling getServerConfiguration for server https://localhost:9443 ...
Cluster received 41 elements
LDAP received 12 elements
ldap_mappings received 0 elements
roles received 6 elements
redis_acls received 3 elements
users received 1 elements
nodes received 1 elements
bdbs received 1 elements
 📖 Success! Retrieved configuration object from REST API.


Running plugin type "detect"

Running plugin "check_nodes"...
Cluster "https://localhost:9443" ...
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Address    ┃ OS Version         ┃ Shards ┃ Status ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 172.17.0.2 │ Ubuntu 18.04.6 LTS │ 2      │ active │
└────────────┴────────────────────┴────────┴────────┘

Running plugin type "correct"

```

# CLI Usage Example 

## Without plugins (smoke test)

You can run `redis_healthcheck` by directly invoking it on your command line with the `start` command. Specify the list of servers to use with the `-s` flag. By default, the tool assumes there is a `serverList.json` file in the same directory. 

```console
~/GitHub/redis_healthcheck$ redis_healthcheck -s ./serverList.json start


 🏥 Oh hey! Let's do a Redis Healthcheck.
 🔌 Doesn't look like you have any plugins.
 🐍 You can install them with pip. (Plugin list: https://TBD/)


~/GitHub/redis_healthcheck$ 
```

Success! Nothing happened -- the base installation has no plugins, so there's nothing to do.

## With plugins

Let's assume you have at least 1 plugin installed. When you run the `redis_healthcheck start` command, you will see a table of all the plugins that the healthcheck app can see:

```console
~/GitHub/redis_healthcheck$ redis_healthcheck start
```

```console


 🏥 Oh hey! Let's do a Redis Healthcheck.
 🔌 I'm seeing 2 plugins on this system:
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Version      ┃ Plugin Name             ┃ Project Name                                  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0.0.1        │ check_nodes             │ RE-Healthcheck-Plugin-Node-Status             │
│ 0.0.1        │ collector_configuration │ RE-Healthcheck-Plugin-Configuration-Collector │
└──────────────┴─────────────────────────┴───────────────────────────────────────────────┘
Loading plugin check_nodes...
Loading plugin collector_configuration...

```

# Usage options

## Application usage

```console
~/GitHub/redis_healthcheck$ redis_healthcheck --help
```

```console
Usage: redis_healthcheck [OPTIONS] COMMAND [ARGS]...

  Redis Enterprise Healthcheck Tool

Options:
  -s, --serverList FILE  JSON containing list of servers [{fqdn, username,
                         password},{...},...] of each managed Redis Enterprise
                         cluster.
  --help                 Show this message and exit.

Commands:
  start  Run Redis Healthcheck from CLI

```

# Developing plugins

The plugin `check_nodes` in the directory `reht_plugin_nodestatus` is a good example of a simple plugin. 

Here's the basic structure of a plugin:

```
.
└── my_plugin/
    ├── src/
    │   └── redis_healthcheck/
    │       ├── __init__.py
    │       └── plugins/
    │           ├── __init__.py
    │           └── my_plugin_code/
    │               ├── __init__.py
    │               ├── collect.py
    │               ├── detect.py
    │               └── correct.py
    ├── setup.py
    └── README.md   
```

It's somewhat cluttered-looking due to the necessary evil of `__init__.py` files. These are required at each directory level by `pip`.

The logic of your plugin will generally go into the `detect.py` file. If you aren't collecting data for the system or fixing anything, you can leave those `collect.py` and `correct.py` out of the project.

Your plugin tells `pip` about the plugin in the `setup.py` file:

```python
from setuptools import setup

setup(
    name="RE Healthcheck Plugin - Node Status",
    version="0.0.1",
    description="Check the nodes status - a plugin for RE Healthcheck",
    author="Matthew Royal",
    author_email="matthew.royal@redis.com",
    url="https://github.com/masyukun",
    packages=[
        "redis_healthcheck",
        "redis_healthcheck.plugins",
        "redis_healthcheck.plugins.my_plugin_code",
    ],
    package_dir={"": "src"},
    install_requires=[
        "future",
        "requests",
        "rich",
    ],
    entry_points={
        'redis_healthcheck_plugin': [
            'my_plugin_name = redis_healthcheck.plugins.my_plugin_code.detect:plugin_metadata',
        ],
    },
)
```

The only things you'll need to modify in `setup.py` are the `packages`, `install_requires`, and `entry_points`:
* `packages` - Make sure the last package in the list reflects your actual directory name for the plugin. This can be anything, but I've learned that Python **HATES** hyphens in names, so avoid those.
* `install_requires` - Other `pip` packages that your project uses. These will be installed as prerequisites for your project.
* `entry_points` -
  * This is how the base healthcheck application finds your plugin: it use the Python `pkg_resources` library to find every entrypoint under `redis_healthcheck_plugin`. 
    * FYI More about this plugin framework: https://www.vinnie.work/blog/2021-02-16-python-plugin-pattern/
  * Change the name on the left-hand side of the assignment to the name you want folks to see in the plugin table when healthcheck is run.
  * Change the dotted directory path on the right-hand side of the assignment with the directory structure of your project. `plugin_metadata` is the function run in the `detect.py` file to provide an entry point that returns a metadata object.


  