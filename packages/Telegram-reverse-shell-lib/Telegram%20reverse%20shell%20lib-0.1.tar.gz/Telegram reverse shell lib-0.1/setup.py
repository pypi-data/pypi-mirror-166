import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


# setup to pypi.org :
# python setup.py sdist bdist_wheel
# twine upload  dist/*


# Package meta-data.
NAME = 'Telegram reverse shell lib'
DESCRIPTION = 'A Python library for inserting an reverse shell attached to Telegram in any Python application.'
URL = "https://github.com/TorhamDev/telegram-reverse-shell-lib"
EMAIL = 'torhamdev@gmail.com'
AUTHOR = 'Torham'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = "0.1"
KEYWORDS = [
    'python reverse shell',
    'generate reverse shell',
    'telegram',
    'telegram reverse shell',
    'python reverse shell',
]
# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))


try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    extras_require=EXTRAS,
    include_package_data=True,
    license='gpl-3.0',
    keywords=KEYWORDS,
    classifiers=[

        # Again, pick a license
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",        
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
    install_requires = [
        "beautifulsoup4==4.11.1",
        "bs4==0.0.1",
        "psutil==5.9.2",
        "requests==2.28.1",
    ]
)
