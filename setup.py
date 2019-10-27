from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="part_map",
    version="1.2.4",
    description="Part Visualizer",
    long_description=readme(),
    url="https://github.com/jdpatt/part_map",
    author="David Patterson",
    license="MIT",
    python_requires=">=3.7",
    packages=["part_map"],
    install_requires=["openpyxl", "Click", "natsort", "PySide2"],
    entry_points={"console_scripts": ["part-map = part_map.part_map:cli"]},
    zip_safe=False,
)
