from setuptools import setup, find_packages
  
# with open('requirements.txt') as f:
#     requirements = f.readlines()
  
long_description = 'Sample Package made for a demo \
      of its making for the jc3wrld999 Article.'
  
setup(
        name ='w24thr',
        version ='1.0.0',
        author ='jc3wrld999',
        author_email ='jc3wrld999@gmail.com',
        url ='https://github.com/jc3wrld999/w24thr',
        description ='Demo Package for w24thr Article.',
        long_description = long_description,
        # long_description_content_type ="text/markdown",
        license ='MIT',
        packages = ['test'],
        # entry_points ={
        #     'console_scripts': [
        #         'gfg = w24thr.gfg:main'
        #     ]
        # },
        # classifiers =(
        #     "Programming Language :: Python :: 3",
        #     "License :: OSI Approved :: MIT License",
        #     "Operating System :: OS Independent",
        # ),
        keywords ='test',
        install_requires = [],
        zip_safe = False
)