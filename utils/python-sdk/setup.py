import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pipdu',
    packages=['pipdu'],
    version='0.0.0',
    license='MIT',
    description='PiPDU python SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mircea-Pavel Anton',
    author_email='contact@mirceanton.com',
    url='https://gitlab.com/mirceanton/piPDU/-/tree/main/utils/python-sdk',
    project_urls={
        "Bug Tracker": "https://gitlab.com/mirceanton/piPDU/-/issues"
    },
    install_requires=['prometheus_client', 'requests', 'pyyaml'],
    keywords=["pypi", "pipdu", "mirceanton"],
)
