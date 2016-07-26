def SKU_exists(api_session, sku):
    """Checks if sku has been used as a product SKU """
    from linnapi.api_requests.sku_exists import SKUExists
    request = SKUExists(api_session, sku)
    return request.response_dict


def get_new_SKU(api_session):
    """Return unsed product SKU."""
    from linnapi.api_requests.inventory.get_new_sku import GetNewSKU
    request = GetNewSKU(api_session)
    return request.sku


def is_guid(guid):
    import re
    regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                        '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
    match = regex.match(guid)
    return bool(match)


def get_stock_id_by_SKU(api_session, sku):
    from linnapi.api_requests.inventory.inventory_view import InventoryView
    from linnapi.api_requests.inventory.inventory_view_filter \
        import InventoryViewFilter
    from linnapi.api_requests.inventory.get_inventory_items \
        import GetInventoryItems

    view = InventoryView()
    view.filters.append(InventoryViewFilter(
        field='String',
        value=sku,
        condition='Equals',
        filter_name='SKU',
        filter_name_exact=''
    ))
    response = GetInventoryItems(api_session, view=view)
    return response.response_dict['Items'][0]['Id']


def get_order_number(api_session, order_number):
    from linnapi.api_requests.orders.\
        get_open_order_id_by_order_or_reference_id import \
        GetOpenOrderIDByOrderOrReferenceID
    from linnapi.orders import OpenOrder
    request = GetOpenOrderIDByOrderOrReferenceID(api_session, order_number)
    if is_guid(request.response_dict):
        order_id = request.response_dict
        try:
            order = OpenOrder(api_session, load_order_id=order_id)
        except:
            order = None
        return order
    else:
        return None


def get_inventory_item(api_session, stock_id=None, sku=None):
    from linnapi.inventory import InventoryItem
    if stock_id is None and sku is None or stock_id is not None and \
            sku is not None:
        raise ValueError("Either stock_id or sku should be supplied")
    if sku is not None:
        stock_id = get_stock_id_by_SKU(api_session, sku)
    return InventoryItem(api_session, load_stock_id=stock_id)


def get_export(api_session, script_id, parameters=[]):
    import linnapi.api_requests
    import lstools
    request = linnapi.api_requests.ExecuteCustomScriptCSV(
        api_session, script_id, parameters)
    table = lstools.Table(filename=request.export_url)
    return table


def get_linking_table(api_session):
    table = get_export(api_session, 14)
    return table


def make_linnworks_date_time(year, month, day, hour=0, minute=0, second=0):
    """Creates a date time string recognised by Linnworks API.

    Args:
        year (int)(str): Four digit year.
        month (int)(str): Month Number. Example - January would be 1.
        day (int)(str): Number of day in month.

    Returns:
        str: Date time string formatted for Linnworks.

    """
    year = str(year)
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    hour = str(hour).zfill(2)
    minute = str(minute).zfill(2)
    second = "%0.3f" % float(second)
    second = second.zfill(6)
    linnworks_date = ''.join([
        year, '-', month, '-', day, 'T', hour, ':', minute, ':', second, 'Z'])
    return linnworks_date


def get_inventory(api_session, location='Default'):
    from linnapi.inventory.inventory import Inventory
    from linnapi.inventory.extended_property import ExtendedProperty
    inventory = Inventory(api_session, load=True)
    inventory_export = get_export(
        api_session, script_id=8, parameters=[
            {"Type": "Select", "Name": "locationName", "Value": "Default"}])
    extended_properties_export = get_export(
        api_session, script_id=57, parameters=[
            {"Type": "String", "Name": "SKU", "Value": ""},
            {"Type": "String", "Name": "Property", "Value": ""}])
    inventory_lookup = {}
    for row in inventory_export:
        inventory_lookup[row['SKU']] = row
    extended_properties_lookup = {}
    for row in extended_properties_export:
        if row['SKU'] not in extended_properties_lookup:
            extended_properties_lookup[row['SKU']] = []
        extended_properties_lookup[row['SKU']].append(row)
    for item in inventory:
        i_row = inventory_lookup[item.sku]
        item.title = i_row['ItemTitle']
        item.meta_data = i_row['ItemDescription']
        item.retail_price = float(i_row['RetailPrice'])
        item.purchase_price = float(i_row['PurchasePrice'])
        item.weight = float(i_row['Weight'])
        item.barcode = i_row['BarcodeNumber']
        item.height = float(i_row['DimHeight'])
        item.width = float(i_row['DimWidth'])
        item.depth = float(i_row['DimDepth'])
        item.tax_rate = float(i_row['TaxRate'])
        item.category = api_session.categories[i_row['CategoryName']]
        try:
            item.postage_service = api_session.postage_services[
                i_row['DefaultPostalService']]
        except:
            pass
        item.package_group = api_session.package_groups[
            i_row['DefaultPackagingGroup']]
        item.available = i_row['Available']
        item.bin_rack = i_row['BinRack']
        if item.sku in extended_properties_lookup:
            for e_row in extended_properties_lookup[item.sku]:
                new_extended_property = ExtendedProperty(
                    property_type=e_row['PropertyType'],
                    value=e_row['PropertyValue'], name=e_row['Property'],
                    item_stock_id=item.stock_id)
                item.extended_properties.append(new_extended_property)


def get_order_id(api_session, order_number):
    from linnapi.api_requests import GetOpenOrderIDByOrderOrReferenceID
    from linnapi.api_requests import SearchProcessedOrdersPaged
    open_order_request = \
        GetOpenOrderIDByOrderOrReferenceID(
            api_session, order_number)
    open_order_request.response.raise_for_status()
    if open_order_request.response.text == 'null':
        processed_order_request = \
            SearchProcessedOrdersPaged(
                api_session, order_number, date_type='ALLDATES',
                exact_match=True, search_field='nOrderId')
        if len(processed_order_request.response_dict['Data']) == 1:
            return processed_order_request.response_dict[
                'Data'][0]['pkOrderID']
        else:
            return None
    else:
        return open_order_request.response_dict
