import requests
import collections
from summary import Summary


class SmmryAPIException(Exception):
    pass


class SmmryAPI:

    def __init__(self, key):
        self.key = key
        self.max = 40  # Max number of sentences
        self.endpoint = 'http://api.smmry.com/'

    def check_length(self, params):

        if params.get('SM_LENGTH'):
            if params['SM_LENGTH'] > self.max:
                params['SM_LENGTH'] = self.max

        return params

    def summarize(self, url, **kwargs):

        kwargs = {k.upper(): v for k, v in kwargs.items()}

        # "Note: The parameter &SM_URL= should always be at the end of the
        # request url to avoid complications" (see https://smmry.com/api).
        params = collections.OrderedDict(kwargs)
        params.update({'SM_API_KEY': self.key})
        params.update({'SM_URL': url})
        params.move_to_end('SM_URL')

        params = self.check_length(params)

        response = requests.get(self.endpoint, params=params)
        response.close()

        smmry_dict = response.json()

        if smmry_dict.get('sm_api_error'):
            raise SmmryAPIException("%s: %s" % (smmry_dict['sm_api_error'], smmry_dict['sm_api_message']))

        smmry_dict['sm_api_content'] = smmry_dict['sm_api_content'].strip()

        return Summary(smmry_dict, params, response)
