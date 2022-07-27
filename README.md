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


## Installing plug-ins



# CLI Usage Example 

You can run `redis_healthcheck` by directly invoking it on your command line with the `start` command. Specify the list of servers to use with the `-s` flag. By default, the tool assumes there is a `serverList.json` file in the same directory. 

```console
~/GitHub/redis_healthcheck$ redis_healthcheck -s ./serverList.json start


 🏥 Oh hey! Let's do a Redis Healthcheck.
 🔌 Doesn't look like you have any plugins.
 🐍 You can install them with pip. (Plugin list: https://TBD/)


~/GitHub/redis_healthcheck$ 
```

Success! Nothing happened -- the base installation has no plugins, so there's nothing to do.

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
