from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Create CSS text color waves for your project.'

# Setting up
setup(
    name="css-color-wave",
    version=VERSION,
    author="loki#4770",
    author_email="<rugalu29@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'css', 'html', 'color', 'color wave'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)