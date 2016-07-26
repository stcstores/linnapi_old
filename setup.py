#!/usr/bin/env python

from distutils.core import setup

setup(name='linnapi',
      version='1.0',
      description='Wrapper for linnworks.net API',
      author='Luke Shiner',
      author_email='luke@lukeshiner.com',
      url='http://linnapi.lukeshiner.com',
      packages=[
        'linnapi',
        'linnapi.api_requests',
        'linnapi.api_requests.import_export',
        'linnapi.api_requests.inventory',
        'linnapi.api_requests.inventory.extended_properties',
        'linnapi.api_requests.inventory.images',
        'linnapi.api_requests.inventory.update_inventory',
        'linnapi.api_requests.orders',
        'linnapi.api_requests.processed_orders',
        'linnapi.api_requests.settings',
        'linnapi.inventory',
        'linnapi.orders',
        'linnapi.settings'],
    package_data={'': ['config.json']})
