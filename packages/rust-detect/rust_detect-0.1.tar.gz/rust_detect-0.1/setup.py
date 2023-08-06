from gettext import install
import setuptools

make_package=setuptools.setup(
    name="rust_detect",
    version="0.1",
    author=["rohan"],
    description=("a simple rust detection technique using opencv tool which detects paricular rust from an image"),
    license="MIT",
   packages = setuptools.find_packages(), python_requires='>=3.6',
   install_requires=["opencv-python","numpy"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],   
    )
    