"""Searches processed orders """

from linnapi.api_requests.request import Request


class SearchProcessedOrdersPaged(Request):
    url_extension = '/api/ProcessedOrders/SearchProcessedOrdersPaged'

    def __init__(
            self, api_session, search_term, from_date='0-00-0000 0:0:0',
            to_date='0-00-0000 0:0:0', date_type='ALLDATES', exact_match=True,
            page_num=1, num_entries_per_page=12,
            search_field='nOrderId'):
        self.search_term = search_term
        self.from_date = from_date
        self.to_date = to_date
        self.date_type = date_type
        self.exact_match = exact_match
        self.page_num = page_num
        self.num_entries_per_page = num_entries_per_page
        self.search_field = search_field
        super().__init__(api_session)

    def get_data(self):
        data = {
            'searchTerm': self.search_term,
            'dateType': self.date_type,
            'exactMatch': str(self.exact_match).lower(),
            'from': self.from_date,
            'numEntriesPerPage': str(self.num_entries_per_page),
            'pageNum': str(self.page_num),
            'searchField': self.search_field,
            'to': self.to_date
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
