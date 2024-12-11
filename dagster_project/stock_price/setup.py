from setuptools import find_packages, setup

setup(
    name="stock_price",
    packages=find_packages(exclude=["stock_price_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
