from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["bin/*"]

setup(name = "basiclib123",
    version = "102",
    description = "Basic programmig library.",
    author = "Veljko Miljanic",
    author_email = "veljkomilj@gmail.com",
    # url = "NA",
    packages = ['basic'],
    package_data = {'basic' : files },
    scripts = [],
    long_description = """Basic programming library.""", 
    #
    #This next part it for the Cheese Shop, look a little down the page.
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
    install_requires=[
        "<ctypes>",
        "<atexit>",
        "<platform>",
        "<os>",
        "<math>",
        "<time>"
    ],
) 
