#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dbt-bigquery-alvin"
package_version = "0.0.1"
description = """The alvinadapter bigquery adapter plugin for dbt"""

# this package needs at least dbt-bigquery version 1.2.0
setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author="Alvin",
    author_email="tech@alvin.ai",
    url="http://alvin.ai",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        "dbt-core>=1.2.0",
        "dbt-bigquery>=1.2.0",
        "alvin-integration[dbt]>=0.15.12",
    ],
)
