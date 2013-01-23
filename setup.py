from setuptools import setup, find_packages
import sys, os

version = '3.1.6'

setup(name='uvckickstart',
      version=version,
      description="Templates for Starting an UVC-Site Add on",
      long_description=""" description """,
      author='Christian Klinger',
      author_email='cklinger@novareto.de',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      url="http://uvwebcommunity.bg-kooperation.de",
      install_requires=[
          'ZopeSkel==2.21.2',
	  'grokproject>=2.2',
	  'zc.buildout',
          'zest.releaser',
      ],
    entry_points=
        {'paste.paster_create_template': 
	        ['uvcaddon = uvckickstart:UVCAddOn',
		 'uvcproject = uvckickstart:UVCProject'],
	 'console_scripts': 
	     ['uvcproject = uvckickstart.uvcproject:main',
	      'uvcaddon = uvckickstart.uvcaddon:main'],
	},
      )
