import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testcases_executor",
    version="0.0.1",
    author="JBthePenguin",
    author_email="jbthepenguin@netcourrier.com",
    description="An executor of groups of unittest.TestCase subclasses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBthePenguin/TestCasesExecutor",
    packages=setuptools.find_packages(),
    package_data={'testcases_executor': ['tc_reporter/templates/*.html']},
    include_package_data=True,
    install_requires=['jinja2'],
    license='LICENSE',
    python_requires='>=3.7.5',
)
