from setuptools import setup, find_packages

setup(
    name="ducket",
    version="0.1.4",
    packages=find_packages(where="src"),
    include_package_data=True,
    package_dir={"": "src"},
    description="a dependency inversion python package for using bucket storage minio",
    author="mopoy",
    author_email="mopoy.code@gmail.com",
    url="https://github.com/sudomopoy/ducket-py",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    dependency_links=[],
    install_requires=[
        "minio==7.2.15",
    ],
)
