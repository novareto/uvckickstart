from setuptools import setup, find_packages

version = '3.3.2.dev0'

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
          'grokproject>=2.9',
          'zc.buildout',
          'zest.releaser',
          'setuptools>=7.0'
      ],
      entry_points=
      {'paste.paster_create_template':
       ['uvcaddon = uvckickstart:UVCAddOn',
        'uvcproject = uvckickstart:UVCProject',
        'uvcploneaddon = uvckickstart:UVCPloneAddon',
        'uvclight = uvckickstart:UVCLight',
        'gatekeeper = uvckickstart:Gatekeeper'],
       'console_scripts':
       ['uvcproject = uvckickstart.uvcproject:main',
        'uvclight = uvckickstart.uvclight:main',
        'gatekeeper = uvckickstart.gatekeeper:main',
        'uvcploneaddon = uvckickstart.uvcploneaddon:main',
        'uvcaddon = uvckickstart.uvcaddon:main'],
       },
      )
