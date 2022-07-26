from setuptools import setup

setup(
    name="redis_healthcheck",
    version="0.0.1",
    description="Redis Enterprise Healthcheck Tool.",
    author="Matthew Royal",
    author_email="matthew.royal@redis.com",
    url="https://github.com/masyukun",
    packages=[
        "redis_healthcheck",
    ],
    package_dir={"": "src"},
    install_requires=[
        "future",
        "rich",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'redis_healthcheck = redis_healthcheck.cli:cli',
        ],
    },
)
