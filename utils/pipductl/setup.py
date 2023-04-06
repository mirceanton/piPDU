import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pipductl',
    packages=['pipductl'],
    version='0.0.0',
    license='MIT',
    description='PiPDU commandline utility',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mircea-Pavel Anton',
    author_email='contact@mirceanton.com',
    url='https://gitlab.com/mirceanton/piPDU/-/tree/main/utils/pipductl',
    project_urls={
        "Bug Tracker": "https://gitlab.com/mirceanton/piPDU/-/issues"
    },
    install_requires=['pipdu_sdk', 'click'],
    keywords=["pypi", "pipdu", "mirceanton"],
)
