from setuptools import setup

setup(name='rsaf',
      version='0.1',
      description='Program to archive files',
      url='https://github.com/xadlien/link-backup',
      author='Daniel Martin',
      author_email='djm24862@gmail.com',
      packages=['rsaf'],
      entry_points = {
          'console_scripts': ['rsaf=rsaf.rsaf:main']
      },
      zip_safe=False)