from setuptools import setup

setup(
    name="RE Healthcheck Plugin - Configuration Collector",
    version="0.0.1",
    description="Get server configuration from Redis Enterprise cluster - a plugin for RE Healthcheck",
    author="Matthew Royal",
    author_email="matthew.royal@redis.com",
    url="https://github.com/masyukun",
    packages=[
        "redis_healthcheck",
        "redis_healthcheck.plugins",
        "redis_healthcheck.plugins.collectors",
        "redis_healthcheck.plugins.collectors.configuration",
    ],
    package_dir={"": "src"},
    install_requires=[
        "future",
        "requests",
        "rich",
    ],
    entry_points={
        'redis_healthcheck_plugin': [
            'collector_configuration = redis_healthcheck.plugins.collectors.configuration.collect:plugin_metadata',
        ],
    },
)