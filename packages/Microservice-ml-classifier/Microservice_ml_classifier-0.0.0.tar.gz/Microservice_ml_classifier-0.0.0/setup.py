import importlib
import setuptools
import codecs
import os


def parse_requirements(filename):
    """
    Load requirements from a pip requirements file ignoring commented requirements
    """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

pkg_name = "Microservice_ml_classifier"
lib = importlib.import_module(pkg_name)
print(dir(lib))

pkg_reqs = parse_requirements("./requirements.txt")
cwd = os.path.dirname(os.path.realpath(__file__))

setuptools.setup(
    name=pkg_name,
    version='0.0.0',
    description="Simple classifier to be used in production",
    long_description=codecs.open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    url=f'https://github.com/VLavado/{pkg_name}',
    author='Victor Lavado',
    license='MIT License',
    packages=setuptools.find_packages(exclude=["*tests*", '*training*', '*dataset*']),
    python_requires='>=3.8',
    install_requires=pkg_reqs,
    package_data={
        pkg_name: [
            os.path.join(cwd, "VERSION")
        ]
    }
)