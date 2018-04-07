from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='part_map',
      version='1.2.1',
      description='Part Visualizer',
      url='https://github.com/jdpatt/part_map',
      author='David Patterson',
      license='MIT',
      packages=['part_map'],
      install_requires=[
        'openpyxl',
        'natsort',
        'PyQt5'
      ],
      entry_points={
        "console_scripts": ['part_map = part_map.part_map:main']
      },
      zip_safe=False)
