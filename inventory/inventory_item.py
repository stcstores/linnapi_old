#!/usr/bin/env python3

"""This module contains the ``InventoryItem`` class to be used as a container
for Linnworks Inventory Items."""

import uuid
import json


class InventoryItem:
    stock_id = None
    json = None
    inventory = None
    sku = ''
    title = ''
    purchase_price = 0
    retail_price = 0
    barcode = ''
    category_id = ''
    category = ''
    depth = ''
    height = ''
    package_group_id = ''
    package_group = ''
    postage_service_id = ''
    postage_service = ''
    tax_rate = 0
    variation_group_name = ''
    weight = 0
    width = 0
    quantity = 0
    meta_data = ''
    extended_properties = None

    def __init__(self, api_session):
        self.api_session = api_session

    def __str__(self):
        return str(self.sku) + ': ' + str(self.title)

    def load_from_json(self, json, inventory):
        self.json = json
        self.inventory = inventory
        self.api_session = self.inventory.api_session
        self.sku = json['SKU']
        self.title = json['Title']
        self.stock_id = json['Id']
        self.purchase_price = json['PurchasePrice']
        self.retail_price = json['RetailPrice']
        self.barcode = json['Barcode']

    def get_stock_id(self):
        """Returns new GUID."""
        self.stock_id = str(uuid.uuid4())

    def create_sku(self):
        """Returns new *SKU*."""
        self.sku = GetNewSKU(self.api_session).sku

    def get_create_inventoryItem_dict(self):
        """Return ``dict`` for use with ``AddInventoryItem`` API request."""
        inventoryItem = {}
        inventoryItem['ItemNumber'] = str(self.sku)
        inventoryItem['ItemTitle'] = str(self.title)
        inventoryItem['BarcodeNumber'] = str(self.barcode)
        inventoryItem['PurchasePrice'] = str(self.purchase_price)
        inventoryItem['RetailPrice'] = str(self.retail_price)
        inventoryItem['Quantity'] = str(self.quantity)
        inventoryItem['TaxRate'] = str(self.tax_rate)
        inventoryItem['StockItemId'] = str(self.stock_id)
        return inventoryItem

    def get_inventoryItem_dict(self):
        """Return ``dict`` for use with ``UpdateInventoryItem`` API request."""
        inventoryItem = {}
        inventoryItem['ItemNumber'] = str(self.sku)
        inventoryItem['ItemTitle'] = str(self.title)
        inventoryItem['BarcodeNumber'] = str(self.barcode)
        inventoryItem['PurchasePrice'] = str(self.purchase_price)
        inventoryItem['RetailPrice'] = str(self.retail_price)
        inventoryItem['Quantity'] = str(self.quantity)
        inventoryItem['TaxRate'] = str(self.tax_rate)
        inventoryItem['StockItemId'] = str(self.stock_id)
        inventoryItem['VariationGroupName'] = str(self.variation_group_name)
        inventoryItem['MetaData'] = str(self.meta_data)
        inventoryItem['CategoryId'] = str(self.category_id)
        inventoryItem['PackageGroupId'] = str(self.package_group_id)
        inventoryItem['PostalServiceId'] = str(self.postage_service_id)
        inventoryItem['Weight'] = str(self.weight)
        inventoryItem['Width'] = str(self.width)
        inventoryItem['Depth'] = str(self.depth)
        inventoryItem['Height'] = str(self.height)
        return inventoryItem

    def create_item(self):
        """Make request to create new *inventory item* on Linnworks server."""
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop is not None)
        inventoryItem = self.get_create_inventoryItem_dict()
        request_url = self.api_session.server + '/api/Inventory/AddInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        return self.api_session.request(request_url, data)

    def update_item(self):
        """Make request to create update existing *inventory item* on Linnworks
        server.
        """
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop is not None)
        inventoryItem = self.get_inventoryItem_dict()
        request_url = self.api_session.server + '/api/Inventory/UpdateInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        return self.api_session.request(request_url, data)

    def update_all(self):
        """Update *inventory item* and it's *extended properties* on Linnworks
        server.
        """
        self.update_item()
        self.extended_properties.update()

    def load_extended_properties(self):
        """Get *extended properties* for item from Linnworks server."""
        self.extended_properties.load()

    def get_extended_properties_dict(self):
        """Return ``dict`` containing *extended_properties* names and
        values.
        """
        properties = {}
        for prop in self.extended_properties:
            if prop.delete is False:
                properties[prop.name] = prop.value
        return properties

    def get_extended_properties_list(self):
        """Return ``list`` containing ``dict``s of *extended properties*
        details.
        """
        properties = []
        for prop in self.extended_properties:
            if prop.delete is False:
                new_prop = {
                    'name': prop.name,
                    'value': prop.value,
                    'type': prop.type,
                    'guid': prop.guid
                }
                properties.append(new_prop)
        return properties

    def create_extended_property(self, name='', value='',
                                 property_type='Attribute'):
        """Add extended property to item.

        Arguments:
            name -- Name of new extended property.
            value -- Value of new extended prperty.

        Keyword Arguments:
            property_type -- Type of new extended property
                Defaults to 'Attribute'.
        """
        prop = _ExtendedProperty(self)
        prop.name = name
        prop.value = value
        prop.type = property_type
        self.extended_properties.append(prop)

    def add_image(self, filepath):
        """Add image to item.

        Arguments:
            filepath -- Path to image to be uploaded.
        """
        upload_response = self.api_session.upload_image(filepath)
        image_guid = upload_response[0]['FileId']
        add_url = self.api_session.server + (
            '/api/Inventory/UploadImagesToInventoryItem')
        add_data = {
            'inventoryItemId': self.stock_id,
            'imageIds': json.dumps([image_guid])}
        add_response = self.api_session.request(add_url, data=add_data)
        return add_response
