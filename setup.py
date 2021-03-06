from pathlib import Path

import setuptools


setuptools.setup(
    name="powerranger",
    version="0.0.2",
    url="https://github.com/clayboone/powerranger.git",
    author="Clay Boone",
    author_email="tener.hades@gmail.com",
    description="A ranger-inspired file manager for PowerShell.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        "console_scripts": [
            "powerranger=powerranger.powerranger:main",
        ],
    },
)
