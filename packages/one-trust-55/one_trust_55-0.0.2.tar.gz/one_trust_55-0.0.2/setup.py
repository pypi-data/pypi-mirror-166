from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'One Trust API Library 55'

# Setting up
setup(
    name="one_trust_55",
    version=VERSION,
    author="Rohit Lobo",
    author_email="rohit.lobo@fifty-five.com",
    url="https://gitlab.55labs.com/rohit.lobo/one_trust_api.git",
    description= DESCRIPTION,
    py_modules=["main","ot_class","file_handle"],
    # package_dir={'':'src'},
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas','requests'],
    keywords=['python', 'one trust', '55']
)
