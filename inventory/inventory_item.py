#!/usr/bin/env python3

"""This module contains the ``InventoryItem`` class to be used as a container
for Linnworks Inventory Items."""

import uuid
import json

from linnapi.api_requests.inventory.get_inventory_column_types \
    import GetInventoryColumnTypes
from linnapi.api_requests.inventory.inventory_view_filter\
    import InventoryViewFilter
from linnapi.api_requests.inventory.get_inventory_items \
    import GetInventoryItems
from linnapi.api_requests.inventory.update_inventory_item \
    import UpdateInventoryItem
from linnapi.api_requests.inventory.get_inventory_item_by_id \
    import GetInventoryItemByID
from linnapi.api_requests.inventory.inventory_view import InventoryView
from .extended_properties import ExtendedProperties
from .extended_property import ExtendedProperty


class InventoryItem:

    def __init__(self, api_session, stock_id=None, sku=None, title=None):
        self.api_session = api_session
        self.extended_properties = ExtendedProperties(self, False)
        if stock_id is not None:
            self.stock_id = stock_id
        if sku is not None:
            self.sku = sku
        if title is not None:
            self.title = title

    def __str__(self):
        return str(self.sku) + ': ' + str(self.title)

    def get_prop(self, prop):
        get_item_request = GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        return item_data[prop]

    def set_prop(self, prop, value):
        get_item_request = GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        item_data[prop] = value
        self.update_item(item_data)

    def get_sku(self):
        return self.get_prop('ItemNumber')

    def get_title(self):
        return self.get_prop('ItemTitle')

    def get_barcode(self):
        return self.get_prop('BarcodeNumber')

    def get_category(self):
        return self.api_session.categories[
            self.get_prop('CategoryId')]

    def get_package_group(self):
        return self.api_session.package_groups[
            self.get_prop('PackageGroupId')]

    def get_postage_service(self):
        return self.api_session.postage_services[
            self.get_prop('PostalServiceId')]

    def get_category_id(self):
        return self.get_prop('CategoryId')

    def get_package_group_id(self):
        return self.get_prop('PackageGroupId')

    def get_postage_service_id(self):
        return self.get_prop('PostalServiceId')

    def get_meta_data(self):
        return self.get_prop('MetaData')

    def get_depth(self):
        return self.get_prop('Depth')

    def get_width(self):
        return self.get_prop('Width')

    def get_height(self):
        return self.get_prop('Height')

    def get_purchase_price(self):
        return self.get_prop('PurchasePrice')

    def get_retail_price(self):
        return self.get_prop('RetailPrice')

    def get_tax_rate(self):
        return self.get_prop('TaxRate')

    def get_quantity(self):
        return self.get_prop('Quantity')

    def set_sku(self, sku):
        return self.set_prop('ItemNumber', str(sku))

    def set_title(self, title):
        return self.set_prop('ItemTitle', str(title))

    def set_barcode(self, barcode):
        return self.set_prop('BarcodeNumber', str(barcode))

    def set_category_id(self, cateogry_id):
        return self.set_prop('CategoryId', str(cateogry_id))

    def set_package_group_id(self, package_group_id):
        return self.set_prop('PackageGroupId', str(package_group_id))

    def set_postage_service_id(self, postage_service_id):
        return self.set_prop('PostalServiceId', str(postage_service_id))

    def set_category(self, cateogry):
        return self.set_prop('CategoryId', str(cateogry_id.guid))

    def set_package_group(self, package_group):
        return self.set_prop('PackageGroupId', str(package_group_id.guid))

    def set_postage_service(self, postage_service):
        return self.set_prop('PostalServiceId', str(postage_service_id.guid))

    def set_meta_data(self, meta_data):
        return self.set_prop('MetaData', str(meta_data))

    def set_depth(self, depth):
        return self.set_prop('Depth', str(float(depth)))

    def set_width(self, width):
        return self.set_prop('Width', str(float(width)))

    def set_height(self, height):
        return self.set_prop('Height', str(float(height)))

    def set_purchase_price(self, purchase_price):
        return self.set_prop('PurchasePrice', str(float(purchase_price)))

    def set_retail_price(self, retail_price):
        return self.set_prop('RetailPrice', str(float(retail_price)))

    def set_tax_rate(self, tax_rate):
        return self.set_prop('TaxRate', int(tax_rate))

    def set_quantity(self, quantity):
        return self.set_prop('Quantity', int(quantity))

    def update_item(self, item_data):
        self.last_update_item_request = UpdateInventoryItem(
            self.api_session, item_data['StockItemId'],
            item_data['ItemNumber'], item_data['ItemTitle'],
            barcode=item_data['BarcodeNumber'],
            purchase_price=item_data['PurchasePrice'],
            retail_price=item_data['RetailPrice'],
            quantity=item_data['Quantity'], tax_rate=item_data['TaxRate'],
            variation_group_name=item_data['VariationGroupName'],
            meta_data=item_data['MetaData'],
            category_id=item_data['CategoryId'],
            package_group_id=item_data['PackageGroupId'],
            postage_service_id=item_data['PostalServiceId'],
            weight=item_data['Weight'], width=item_data['Width'],
            depth=item_data['Depth'], height=item_data['Height'])

    def load_from_stock_id(self, stock_id):
        self.stock_id = stock_id
        self.load_all()

    def load_from_request(self, item_data):
        self.stock_id = item_data['Id']
        self.sku = item_data['SKU']
        self.barcode = item_data['Barcode']
        self.quantity = item_data['StockLevel']
        self.title = item_data['Title']
        self.category = self.api_session.categories[item_data['Category']]
        self.purchase_price = item_data['PurchasePrice']
        self.retail_price = item_data['RetailPrice']
        self.available = item_data['Available']
        self.bin_rack = item_data['BinRack']

    def load_all(self):
        get_item_request = GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        if item_data['PostalServiceId'] \
                != '16a52bf9-47e5-44a2-aa38-15d6742dd84a':
            self.postage_service = self.api_session.postage_services[
                item_data['PostalServiceId']]
        else:
            self.postage_service = self.api_session.postage_services['Default']
        self.sku = item_data['ItemNumber']
        self.barcode = item_data['BarcodeNumber']
        self.depth = item_data['Depth']
        self.height = item_data['Height']
        self.meta_data = item_data['MetaData']
        self.package_group = self.api_session.package_groups[
            item_data['PackageGroupId']]
        self.purchase_price = item_data['PurchasePrice']
        self.tax_rate = item_data['TaxRate']
        self.variation_group_name = item_data['VariationGroupName']
        self.weight = item_data['Weight']
        self.width = item_data['Width']

        locations = self.api_session.locations.ids
        view = InventoryView()
        columns_request = GetInventoryColumnTypes(self.api_session)
        view.columns = columns_request.columns
        view_filter = InventoryViewFilter(
            field='SKU', value=self.sku, condition='equals')
        view.filters = [view_filter]
        inventory_request = GetInventoryItems(
            self.api_session, start=0, count=1, view=view,
            locations=locations)
        self.load_from_request(inventory_request.response_dict['Items'][0])
#       self.load_extended_properties()

    def set_empty_fields_to_default(self):
        from linnapi.functions import get_new_SKU
        if self.title is None or self.title == '':
            raise ValueError("Cannot create item without title")
        if self.stock_id is None:
            self.stock_id = str(uuid.uuid4())
        else:
            stock_id = self.stock_id
        if self.sku is None:
            self.sku = get_new_SKU(self.api_session)
        if self.barcode is None:
            self.barcode = ''
        if self.purchase_price is None:
            self.purchase_price = 0
        if self.retail_price is None:
            self.purchase_price = 0
        if self.available is None:
            self.available = 0
        if self.tax_rate is None:
            self.tax_rate = 0
        if self.variation_group_name is None:
            self.variation_group_name = ''
        if self.meta_data is None:
            self.meta_data = ''
        if self.category is None:
            self.category = self.api_session.categories['Default']
        if self.package_group is None:
            self.package_group = self.api_session.package_groups['Default']
        if self.postage_service is None:
            self.postage_service = self.api_session.postage_services['Default']
        if self.weight is None:
            self.weight = 0
        if self.width is None:
            self.width = 0
        if self.depth is None:
            self.depth = 0
        if self.height is None:
            self.height = 0

    def get_inventory_item_dict(self):
        self.set_empty_fields_to_default()
        item_data = {}
        item_data['ItemNumber'] = str(self.sku)
        item_data['ItemTitle'] = str(self.title)
        item_data['BarcodeNumber'] = str(self.barcode)
        item_data['PurchasePrice'] = str(float(self.purchase_price))
        item_data['RetailPrice'] = str(float(self.retail_price))
        item_data['Quantity'] = int(self.available)
        item_data['TaxRate'] = int(self.tax_rate)
        item_data['StockItemId'] = str(self.stock_id)
        item_data['VariationGroupName'] = str(self.variation_group_name)
        item_data['MetaData'] = str(self.meta_data)
        item_data['CategoryId'] = str(self.category.guid)
        item_data['PackageGroupId'] = str(self.package_group.guid)
        item_data['PostalServiceId'] = str(self.postage_service.guid)
        item_data['Weight'] = str(float(self.weight))
        item_data['Width'] = str(float(self.width))
        item_data['Depth'] = str(float(self.depth))
        item_data['Height'] = str(float(self.height))
        return item_data

    def create_item(self):
        from linnapi.api_requests.inventory.add_inventory_item \
            import AddInventoryItem
        item_data = self.get_inventory_item_dict()
        self.add_item_request = AddInventoryItem(
            self.api_session, item_data['StockItemId'],
            item_data['ItemNumber'], item_data['ItemTitle'],
            barcode=item_data['BarcodeNumber'],
            purchase_price=item_data['PurchasePrice'],
            retail_price=item_data['RetailPrice'],
            quantity=item_data['Quantity'], tax_rate=item_data['TaxRate'],
            variation_group_name=item_data['VariationGroupName'],
            meta_data=item_data['MetaData'],
            category_id=item_data['CategoryId'],
            package_group_id=item_data['PackageGroupId'],
            postage_service_id=item_data['PostalServiceId'],
            weight=item_data['Weight'], width=item_data['Width'],
            depth=item_data['Depth'], height=item_data['Height'])
        self.update_item()

    def update_all(self):
        self.update_item()
        self.extended_properties.update()

    def load_extended_properties(self):
        request = GetInventoryItemExtendedProperties(
            self.api_session, self.stock_id)
        response = request.response_dict
        for extended_property in response:
            new_property = ExtendedProperty(
                property_type=extended_property['PropertyType'],
                value=extended_property['PropertyValue'],
                name=extended_property['ProperyName'],
                property_id=extended_property['pkRowId'],
                item_stock_id=self.stock_id)
            self.extended_properties.append(new_property)

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
