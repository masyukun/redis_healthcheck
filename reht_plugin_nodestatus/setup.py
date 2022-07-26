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
        "redis_healthcheck.plugins.checknodes",
    ],
    package_dir={"": "src"},
    install_requires=[
        "future",
        "requests",
        "rich",
    ],
    entry_points={
        'redis_healthcheck_plugin': [
            'check_nodes = redis_healthcheck.plugins.checknodes.detect:plugin_metadata',
        ],
    },
)