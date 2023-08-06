from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()
setup(
  name = 'dj-deploy-cli',
  packages = ['dj-deploy-cli'],
  version = '0.1',
  license='MIT',
  description = 'Generate your Procfile, runtime.txt and requirements.txt from the CLI.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Leo Mbm',
  author_email = 'leo.j.mbm@gmail.com',
  url = 'https://github.com/LeoMbm/django-deploy-cli',
  download_url = 'https://github.com/LeoMbm/django-deploy-cli/archive/refs/tags/v0.1.tar.gz',
  keywords = ['Python', 'Django', 'CommandLine'],
  install_requires=[
          'sys',
          'platform',
          'pyfiglet',
          'termcolor',
          'inquirer',
          'time',
          'os',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.10',
  ],
)