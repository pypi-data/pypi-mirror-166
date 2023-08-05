from setuptools import setup, find_packages 
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "brewt" / "src" / "README.md").read_text

setup(
    name="brewt",
    version="1.1.0",
    description="a brewing tool for CivCraft",
    author="omokami",
    url="https://github.com/okosuno/brewt",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities"
    ],
    keywords="civcraft, civmc",
    python_requires=">=3.8",
    install_requires=["rich", "rapidfuzz"],
    entry_points={
        "console_scripts": [
            "brewt=brewt.brewt:main",
        ]
    },
    project_urls={
    }
)
