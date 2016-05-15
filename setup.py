import re
from setuptools import setup

version = re.search(r'^__version__\s*=\s*"(.*)"$',
                    open("qaamus/__init__.py", "r").read(), re.M).group(1)

setup(name='qaamus',
      version=version,
      description='qaamus, penterjemah indonesia arab. Melalui web qaamus.com ',
      url="https://github.com/ihfazhillah/qaamus-python",
      author='IbnuAmin',
      author_email='mihfazhillah@gmail.com',
      license='MIT',
      packages=['qaamus'],
      entry_points={"console_scripts": ["qaamus = qaamus.cli:main"]},
      keywords=['qaamus', 'terjemah', 'kamus', 'indonesia arab'],
      install_requires=['requests', 'bs4'],
      include_package_data=True,
      zip_safe=False)
