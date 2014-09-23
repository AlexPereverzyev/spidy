
''' High-level HTTP communication interface. '''

import re
import codecs
import httplib

from spidy.common.errors import WebException

WEB_URL_PATTERN     = re.compile('''([a-z]{3,9}:\/\/|[a-z]{3,9}:\/\/www\.|www\.)([\w.-]+)((?:\/[\w\/:@\-_~.%!$&'()*+=,;]*)?(?:\?[\w\-\+=&;%@._]*)?(?:#[\w\/:?@\-_~.%!$&'()*+=,;]*)?)''')
WEB_GET             = 'GET'
WEB_POST            = 'POST'
WEB_HTTPS           = 'https'
WEB_SUCCESS         = [200, 201, 202, 203, 204]
WEB_REDIRECT        = [300, 301, 302, 303]
WEB_REDIRECT_MAX    = 5
WEB_HEAD_LOCATION   = 'location'
WEB_HTML_HEADERS    = {'Accept':'text/html,application/xhtml+xml,application/xml',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Connection':'keep-alive',
                       'Cache-Control':'max-age=0'}

class WebClient(object):
    ''' Basic HTTP client for GET and POST requests. '''
    
    def get(self, url_string, headers):
        ''' Sends GET request, handles redirects automatically. ''' 
        doc = None
        location = url_string
        
        # merge headers with default ones
        rq_headers = {}
        for hk in WEB_HTML_HEADERS.keys():
            rq_headers[hk] = WEB_HTML_HEADERS[hk]
        if headers != None:
            for hk in headers.keys():
                rq_headers[hk] = headers[hk]
            
        redirects = 0
        while True:
            # decompose URL
            m = WEB_URL_PATTERN.match(location)
            if m == None:
                if conn != None: conn.close()
                raise WebException('WebClient: invalid document URL')
                
            schema = m.group(1)
            domain = m.group(2)
            path = m.group(3)

            # get the document
            try:
                conn = None
                if WEB_HTTPS in schema.lower():
                    conn = httplib.HTTPSConnection(domain)
                else:
                    conn = httplib.HTTPConnection(domain)
                conn.request(WEB_GET, path, headers = rq_headers)
                resp = conn.getresponse()
                
            except Exception as e:
                conn.close()
                raise e
            
            # process status
            if resp.status in WEB_REDIRECT:
                if redirects > WEB_REDIRECT_MAX:
                    conn.close()
                    raise WebException('WebClient: exceeded max number of HTTP redirects')
                location = resp.getheader(WEB_HEAD_LOCATION)
            
            elif resp.status in WEB_SUCCESS:
                doc = unicode(resp.read(), 'UTF8', 'ignore')
                conn.close()
                break
            
            else:
                conn.close()
                raise WebException('WebClient: GET request failed')
            
        return doc

    def post(self, url, headers, body):
        ''' Sends POST request, handles redirects automatically. Not implemented yet. ''' 
        pass