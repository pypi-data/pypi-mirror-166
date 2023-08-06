from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    
    name="dummy_project",  # Required
    
    version="2.0.2",  # Required
    
    description="A sample Python project",  # Optional
   
    long_description=long_description,  # Optional

    long_description_content_type="text/markdown",  # Optional (see note above)
    
    url="https://github.com/pypa/sampleproject",  # Optional
   
    author="Manish kumar",  # Optional
   
    author_email="er.manishsingh03@gmail.com",  # Optional
    
    classifiers=[ 
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],

    keywords="sample, setuptools, development",  # Optional
   
    package_dir={"": "src"},  # Optional
    
    packages=find_packages(where="src"),  # Required
   
    python_requires=">=3.7, <4",
   
   
)
