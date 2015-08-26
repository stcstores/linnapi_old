#!/usr/bin/env python3

"""This module contains the main ``LinnworksAPI`` class, the wrapper class for
the linnworks.net API.
"""

import requests
import json
import uuid
from pprint import pprint

from . inventory_item import InventoryItem as InventoryItem
from . inventory import Inventory as Inventory

class LinnworksAPI:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """
    
    def __init__(self, password=None):
        """Authenticate user and set ``self.token`` and ``self.server``
        variables. If password argument is None request password form user as
        ``input()``.
        
        Keyword Arguments:
            username -- Linnworks username (Default None)
            password -- Linnworks password (Default None)
        """
        self.session = requests.Session()
        self.username = 'stcstores@yahoo.com'
        if password == None:
            self.password = input('Linnworks Password: ')
        else:
            self.password = password
        self.get_token()
        

    def make_request(self, url, data=None, to_json=True):
        """Request resource URL
        
        Arguments:
            url (str): URL of resource to be requested.
            
        Keyword arguments:
            data --  dict containing GET request variables. (Default None)
            to_json -- If True method returns parsed JSON. (Default True)
                
        Returns:
            If to_json is True return response as parsed JSON. Otherwise return
            requests.Request object.
        """
        response = self.session.get(url, params=data)
        if to_json == True:
            return response.json()
        else:
            return response

    def request(self, url, data=None, to_json=True):
        """Add authentication variables and make API request.
        
        Arguments:
            url -- URL to request.
            
        Keyword Arguments:
            data -- ``dict`` of GET variables (Default None)
            to_json -- If True method returns parsed JSON. (Default True)
            
        Returns:
            If to_json is True return response as parsed JSON. Otherwise return
            requests.Request object.
        """
        if data == None:
            data = {}
        data['token'] = self.token
        return self.make_request(url, data, to_json=to_json)

    def get_token(self):
        """Make authentication requests and set ``self.token`` and
        ``self.server`` accordingly.
        """
        login_url = 'https://api.linnworks.net//api/Auth/Multilogin'
        auth_url =  'https://api.linnworks.net//api/Auth/Authorize'
        login_data = {'userName' : self.username, 'password' : self.password}
        multilogin = self.make_request(login_url, login_data)
        self.user_id = multilogin[0]['Id']
        auth_data = login_data
        auth_data['userId'] = self.user_id
        authorize = self.make_request(auth_url, auth_data)
        self.token = authorize['Token']
        self.server = authorize['Server']
        
    def create_guid(self):
        """Return new ``GUID``."""
        return str(uuid.uuid4())
    

    def get_category_info(self):
        """Return *category* information as ``dict``."""
        url = self.server + '/api/Inventory/GetCategories'
        response = self.request(url)
        categories = []
        for category in response:
            new_category = {}
            new_category['name'] = category['CategoryName']
            new_category['id'] = category['CategoryId']
            categories.append(new_category)
        return categories
    

    def get_category_names(self):
        """Return *category* names as ``list``."""
        category_names = []
        for category in self.get_category_info():
            category_names.append(category['name'])
        return category_names
    

    def get_category_ids(self):
        """Return *category* IDs as ``list``."""
        category_ids = []
        for category in self.get_category_info():
            category_ids.append(category['id'])
        return category_ids
    
    
    def get_packaging_group_info(self):
        """Return *packaging group* information as ``dict``."""
        url = self.server + '/api/Inventory/GetPackageGroups'
        response = self.request(url)
        packaging_groups = []
        for group in response:
            new_group = {}
            new_group['id'] = group['Value']
            new_group['name'] = group['Key']
            packaging_groups.append(new_group)
        return packaging_groups
    
    
    def get_packaging_group_names(self):
        """Return *packaging group* names as ``list``."""
        packaging_group_names = []
        for group in self.get_packaging_group_info():
            packaging_group_names.append(group['name'])
        return packaging_group_names
    
    
    def get_shipping_method_info(self):
        """Return *shipping method* information and return as ``dict``."""
        url = self.server + '/api/Orders/GetShippingMethods'
        response = self.request(url)
        shipping_methods = []
        for service in response:
            for method in service['PostalServices']:
                new_method = {}
                new_method['vendor'] = method['Vendor']
                new_method['id'] = method['pkPostalServiceId']
                new_method['tracking_required'] = method['TrackingNumberRequired']
                new_method['name'] = method['PostalServiceName']
                shipping_methods.append(new_method)
        return shipping_methods
    
    
    def get_shipping_method_names(self):
        """Return *shipping method* as ``list``."""
        shipping_group_names = []
        for group in self.get_shipping_method_info():
            shipping_group_names.append(group['name'])
        return shipping_group_names
    
    
    def get_location_info(self):
        """Return *location* names and IDs and return as ``dict``."""
        url = self.server + '/api/Inventory/GetStockLocations'
        response = self.request(url)
        locations = []
        for location in response:
            new_location = {}
            new_location['name'] = location['LocationName']
            new_location['id'] = location['StockLocationId']
            locations.append(new_location)
        return locations
    
    
    def get_location_names(self):
        """Return *location* names as ``list``."""
        locations = []
        for location in self.get_location_info():
            locations.append(location['name'])
        return locations
    

    def get_location_ids(self):
        """Return *location* IDs as ``list``."""
        locations = []
        for location in self.get_location_info():
            locations.append(location['id'])
        return locations
    

    def get_channels(self):
        """Return *channel* information as ``dict``."""
        url = self.server + '/api/Inventory/GetChannels'
        response = self.request(url)
        channels = []
        for channel in response:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels


    def get_inventory_views(self):
        """Return ``list`` of *inventory views*."""
        url = self.server + '/api/Inventory/GetInventoryViews'
        response = self.request(url)
        return response
    

    def get_new_inventory_view(self):
        """Returns default *inventory view*."""
        url = self.server + '/api/Inventory/GetNewInventoryView'
        response = self.request(url)
        return response
    

    def get_inventory_column_types(self):
        """Return ``list`` of *column types*."""
        url = self.server + '/api/Inventory/GetInventoryColumnTypes'
        response = self.request(url, to_json=to_json)
        return response
    

    def get_inventory_items(self, start=0, count=1, to_json=True, view=None):
        """Rquest *inventory items*.
        
        Keyword arguments:
            start -- Index of first item to be returned. Default 0.
            count -- Number of items to be returned. Default 1.
            view: InventoryView ``JSON`` object to filter results. Default will
                return any item.
            to_json -- If True method returns parsed JSON. (Default True)
            
        Returns:
            If to_json is True return response as parsed JSON. Otherwise return
            requests.Request object.
        """
        if view == None:
            view = self.get_new_inventory_view()
        url = self.server + '/api/Inventory/GetInventoryItems'
        view_json = json.dumps(view)
        locations = json.dumps(self.get_location_ids())
        data = {'view' : view_json,
                'stockLocationIds' : locations,
                'startIndex' : start,
                'itemsCount' : count
                }
        response = self.request(url, data, to_json=to_json)
        return response
    

    def get_inventory_list(self, view=None,start=0, count=None):
        """Return *inventory items* as ``inventory.Inventory`` object.
        
        Keyword arguments:
            start -- Index of first item to be returned. Default 0.
            count -- Number of items to be returned. Default 1.
            view: InventoryView ``JSON`` object to filter results. Default will
                return any item.
            to_json -- If True method returns parsed JSON. (Default True)
        
        Returns:
            ``inventory.Inventory`` object.
        """
        if view == None:
            view = self.get_new_inventory_view()
        if count == None:
            item_count = self.get_item_count()
        else:
            item_count = count
        
        all_items = []
        item_list =  self.get_inventory_items(start=start,
                count=item_count, view=view)['Items']
        
        inventory = Inventory(item_list, self)
        return inventory
    
    
    def get_item_count(self):
        """Return number of items in *inventory*."""
        request = self.get_inventory_items(start=0, count=1, view=None)
        item_count = request['TotalItems']
        return item_count
        
        
    def get_inventory_item_by_id(self, stock_id, inventory_item=True):
        """Returns **inventory item** data for the item with the specifed
        *stock id*.
        
        Arguments:
            stock_id -- GUID of *inventory item*.
            
        Keyword Arguments:
            inventory_item -- If true return ``inventory_item.InventoryItem``.
                Else return parsed ``JSON``.
        
        Returns:
            If inventory_item is True returns ``inventory_item.InventoryItem``.
            Else Parsed ``JSON``.
        """
        url = self.server + '/api/Inventory/GetInventoryItemById'
        data = {'id' : stock_id}
        response = self.request(url, data)
        if inventory_item != True:
            return response
        else:
            item = InventoryItem(self, stock_id)
            item.sku = response['ItemNumber']
            item.title = response['ItemTitle']
            item.purchase_price = response['PurchasePrice']
            item.retail_price = response['RetailPrice']
            item.barcode = response['BarcodeNumber']
            item.category_id = response['CategoryId']
            item.depth = response['Depth']
            item.height = response['Height']
            item.package_group_id = response['PackageGroupId']
            item.postage_service_id = response['PostalServiceId']
            item.tax_rate = response['TaxRate']
            item.variation_group_name = response['VariationGroupName']
            item.weight = response['Weight']
            item.width = response['Width']
            item.quantity = response['Quantity']
            item.meta_data = response['MetaData']
            
            for category in self.get_category_info():
                if category['id'] == item.category_id:
                    item.category = category['name']
            
            for package_group in self.get_packaging_group_info():
                if package_group['id'] == item.package_group_id:
                    item.package_group = package_group['name']
            
            for postage_service in self.get_shipping_method_info():
                if postage_service['id'] == item.postage_service:
                    item.postage_service = postage_service['name']
            
            return item
    
    
    def get_extended_property_names(self):
        """Return ``list`` of *extended property* names."""
        url = self.server + '/api/Inventory/GetExtendedPropertyNames'
        response = self.request(url)
        return response
    

    def get_inventory_item_extended_properties(self, stock_id):
        """Return ``dict`` of *extended properties* names and IDs.
        
        Arguments:
            stock_id -- GUID of *inventory item*.
        """
        url = self.server + '/api/Inventory/GetInventoryItemExtendedProperties'
        data = {'inventoryItemId' : stock_id}
        response = self.request(url, data)
        return response
    
    
    def get_new_sku(self):
        """Return unsed product SKU."""
        url = self.server + '/api/Stock/GetNewSKU'
        response = self.request(url)
        return response
    
    
    def sku_exists(self, sku):
        """Return True if sku exists for item on Linnworks server."""
        url = self.server + '/api/Stock/SKUExists'
        data = {'SKU' : sku}
        response = self.request(url, data)
        return response
    
    
    def upload_image(self, filename, filepath):
        """Upload image file to Linnworks Server.
        
        Arguments:
            filename -- Filename for the image.
            filepath -- Full path to the image.
            
        Returns:
            Server response as parsed JSON. This contains the id assigned to the
            image. This must be used to apply the image to a product.
        """
        url = self.server + '/api/Uploader/UploadFile?type=Image&expiredInHours=24&token='
        url += self.token
        files = {filename : open(filepath, 'rb')}
        response = self.session.post(url, files=files)
        return response
    
    
    def create_variation_group(self, parent_title, variation_guids,
            parent_guid=None, parent_sku=None):
        """Create a variation group.
        
        Arguments:
            parent_title -- Title of new variation group.
            variation_guids -- List of variation group products *stock_ids*.
                
        Keyword Arguments:
            parent_guid -- New guid to be used as pkVariationId. Creates one by
                default.
            parent_sku -- New SKU for the new variation group. Creates one by
                default.
                
        Returns:
            True if server response is empty string. Otherwise returns the
            server response.
        """
        if parent_guid == None:
            parent_guid = self.create_guid()
        if parent_sku == None:
            parent_sku = self.get_new_sku()
        url = self.server + '/api/Stock/CreateVariationGroup'
        template = {}
        template['ParentSKU'] = parent_sku
        template['VariationGroupName'] = parent_title
        template['ParentStockItemId'] = parent_guid
        template['VariationItemIds'] = variation_guids
        data = {'template' : json.dumps(template)}
        response = self.request(url, data)
        if response == '':
            return True
        else:
            return response
    
    
    def get_variation_group_id_by_SKU(self, sku):
        """Return *stock id* for *variation group* with SKU ``sku``."""
        url = self.server + '/api/Stock/SearchVariationGroups'
        data = {}
        data['searchText'] = str(sku)
        data['searchType'] = 'ParentSKU'
        data['entriesPerPage'] = '100'
        data['pageNumber'] = 1
        response = self.request(url, data)
        print(response)
        return response['Data'][0]['pkVariationItemId']
    
        
    def get_variation_group_inventory_item_by_SKU(self, sku):
        """Return ``inventory_item.InventoryItem`` containing *variation group*
        with SKU ``sku``.
        """
        guid = self.get_variation_group_id_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item
    
    
    def get_inventory_item_id_by_SKU(self, sku):
        """Return *stock id* for *inventory item* with SKU ``sku``."""
        view = self.get_new_inventory_view()
        view['Columns'] = []
        _filter = {}
        _filter['Value'] = str(sku)
        _filter['Field'] = 'String'
        _filter['FilterName'] = 'SKU'
        _filter['FilterNameExact'] = ''
        _filter['Condition'] = 'Equals'
        view['Filters'] = [_filter]
        
        response = self.get_inventory_items(view=view)
        stock_id = response['Items'][0]['Id']
        return stock_id
    
    
    def get_inventory_item_by_SKU(self, sku):
        """Return ``inventory_item.InventoryItem`` containing *inventory item*
        with SKU ``sku``.
        """
        guid = self.get_inventory_item_id_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item