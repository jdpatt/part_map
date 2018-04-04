from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='color_map',
      version='0.2',
      description='Visualize the pins you are assigning to a part',
      url='https://github.com/jdpatt/bga_color_map',
      author='David Patterson',
      license='MIT',
      packages=['color_map'],
      install_requires=[
        'openpyxl',
        'natsort',
        'PyQt5'
      ],
      entry_points={
        "console_scripts": ['color_map = color_map.color_map:main']
      },
      zip_safe=False)
