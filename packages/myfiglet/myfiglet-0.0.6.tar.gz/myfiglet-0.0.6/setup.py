import setuptools

setuptools.setup(
    name = "myfiglet",
    author = "Harsh Gupta",
    version='0.0.6',
    author_email = "harshnkgupta@gmail.com",
    description = "FIGlet Using Python",
    long_description="This module can be used to display FIGlet fonts using python. This is a simple,standalone and easy to understand module with zero dependency on external packages.Best use case is, it can be used in unison with different programs to make them more lively and attarctive.Now you can also add colours to figlet fonts (using <colour> argument) to make them more beautiful.Rainbow colour effect can also be generated in figlet fonts using <rainbow=True> argument in display() function.\n\n Syntax: \n\n >>>import myfiglet \n\n >>>myfiglet.display(<input_string>,<symbol>) \n\n Example: >>>myfiglet.display( 'Python' , '%') \n\n Example: >>>myfiglet.display( 'Harsh' , pattern='name') \n\n\nType >>>myfiglet.help() for further help.",
    packages=['myfiglet'],
    install_requires=[]
    )
