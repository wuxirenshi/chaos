import requests
import json
import logging


class Handler(object):
    def __init__(self):
        """
        This class is used to handle interaction towards coffee interface.
        """
        super(Handler, self).__init__()
        logging.warning('Initializing coffeeHandler....')

        # get an active token and get prepared for sending request
        self.coffee_session = requests.session()

    def get_rsp_from_url(self, url, params=None, method='get', data=None):
        logging.warning('when using method {}, header is:\n {} \n data is: \n{}.\n'.
                        format(method, self.coffee_session.headers, data))
        rsp = None

        if 'get' == method:
            rsp = self.coffee_session.get(url, params=params, timeout=10)
        elif 'put' == method:
            rsp = self.coffee_session.put(url, data=json.dumps(data))
        elif 'post' == method:
            rsp = self.coffee_session.post(url, data=json.dumps(data))
        elif 'delete' == method:
            rsp = self.coffee_session.delete(url, data=json.dumps(data))
        else:
            assert 0, 'We only support get/post/put/delete for now!!!'

        logging.warning('\n\n#####\nget rsp from url: \n{} is :\n##### \n{}\n#####\n\ntext is: \n{}\n#####\n'.
                        format(url, repr(rsp), repr(rsp.text)))
        return rsp