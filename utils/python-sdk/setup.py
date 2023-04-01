import setuptools
import os

version = os.environ.get('VERSION')
job_id = os.environ.get('CI_JOB_ID')

if os.environ.get('CI_COMMIT_BRANCH') != os.environ.get('CI_DEFAULT_BRANCH'):
    version = f"{version}-{job_id}"

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pipdu',
    packages=['src'],
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
