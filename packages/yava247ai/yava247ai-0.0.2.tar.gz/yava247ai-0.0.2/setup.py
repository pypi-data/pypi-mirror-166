from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Experiment for tracking'
#LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="yava247ai", 
        version=VERSION,
        author="Ahmad Lutfi Bayu Aji of Labs247",
        #author_email="<youremail@email.com>",
        description=DESCRIPTION,
        #long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['scikit-learn', 'mlflow', 'pyarrow'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
)
