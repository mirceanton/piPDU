import setuptools
import os

version_file = ""
with open('VERSION', 'r') as f:
    version_file = f.read().strip()

if os.environ.get('CI_COMMIT_BRANCH') == os.environ.get('CI_DEFAULT_BRANCH'):
    version = version_file
else:
    version = f"{version_file}-os.environ['CI_COMMIT_TIMESTAMP']"

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pipdu',
    packages=['pipdu'],
    version=version,
    license='MIT',
    description='PiPDU python SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mircea-Pavel Anton',
    author_email='contact@mirceanton.com',
    url='https://gitlab.com/mirceanton/piPDU/-/tree/main/utils/pipdu-pip', 
    project_urls = {
        "Bug Tracker": "https://gitlab.com/mirceanton/piPDU/-/issues"
    },
    install_requires=['prometheus_client', 'requests'],
    keywords=["pypi", "pipdu", "mirceanton"],
)
