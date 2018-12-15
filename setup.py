from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["assets/*"]

setup(name = "wapp",
    version = "1",
    description = "This is weather app to show weather of the entered location.",
    author = "Javed Sayyed",
    author_email = "javedsayyed868@gmail.com",
    url = "NA",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['weatherapp'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'weatherapp' : files },
    #'runner' is in the root.
    scripts = ["wapp"],
    long_description = """This is weather app to show weather of the entered location.""" 
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
) 
