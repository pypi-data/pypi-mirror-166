import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = os.getenv(key="PACKAGE_NAME", default="arora")
version = os.getenv(key="PACKAGE_VERSION", default="1.0.0")
docs_url = os.getenv(key="DOCS_URL", default="https://sleep-revolution.gitlab.io/sleepy/v0.1.2/")

project_urls = {
    "Documentation": docs_url,
}

setuptools.setup(
    name=package_name,
    version=os.getenv(key="PACKAGE_VERSION", default="1.1.0"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sleep Revolution",
    author_email="sleeprevolution@ru.is",
    description="A tool for sleep researcher to preprocess, work, analyze and visualize data",
    packages=setuptools.find_packages(),
    package_data = {"arora": ["data.txt"]},
    py_modules=["find_features", "arora"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ],
    project_urls=project_urls,
    install_requires=["numpy", "pandas", "mne", "scipy"],
    python_requires=">=3.8"
)
