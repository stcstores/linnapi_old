"""Requests list of column types """

from .. request import Request
from . inventory_view_column import InventoryViewColumn


class GetInventoryColumnTypes(Request):
    url_extension = '/api/Inventory/GetInventoryColumnTypes'

    def process_response(self, response):
        self.column_dicts = []
        self.columns = []
        for column in self.response_dict:
            self.column_dicts.append(column)
            new_column = InventoryViewColumn()
            new_column.load_from_dict(column)
            self.columns.append(new_column)
