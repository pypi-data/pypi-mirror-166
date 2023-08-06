"""
    HTTP features for HTTP based backends    
"""

import requests
from pathlib import Path
from pydeen.types import Request, Connector, Result, Backend, Auth

class HTTPRequest(Request):

    def __init__(self, connector: Connector) -> None:
        super().__init__()
        self.headers = {}
        self.params  = {}
        self.result  = None
        self.http_request = None
        self.status_code = 0
        self.connector = connector
        self.payload:str = None

    def get_params(self):
        params = {}
        backend_params = self.connector.get_backend().get_params()
        if len(backend_params) > 0:
            params += backend_params        
        
        if len(self.connector.params) > 0:
            params += self.connector.params

        if len(self.params) > 0:
            params += self.params
        return params

    def get_response_text(self) -> str:
        if self.http_request != None:
            return self.http_request.text
        else: 
            return None    

    def get_response_json(self):
        return self.http_request.json()

    def is_response_availabe(self) -> bool:
        if self.http_request == None:
            return False
        else:
            return True 


    def get_status_code(self) -> int:
        return self.status_code

    def set_result_from_request(self):
        # check http result is given
        self.result = None
        if self.http_request == None:
            return None
        
        # check result type
        try:    
            result = self.http_request.json()
        except:
            result = self.http_request.text
            self.trace("request result is no json. set text")

        if result != None:
            self.result = Result(result)
        return self.result         

    def get(self, path_append="", parameters:dict=None) -> int:
        url = self.connector.build_url(path_append, parameters)
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")

        request = requests.get(url, params=params, headers=self.headers, auth=auth)
        if request == None:
            self.status_code = 500
            self.error(f"request get failed: URL {url}")
        else:
            self.http_request = request
            self.status_code  = request.status_code    
        
        self.trace(f"request get result: {self.status_code}")    
        self.set_result_from_request()
        return self.status_code

    def post(self, payload:str=None, path_append="", parameters:dict=None) -> int:
        url = self.connector.build_url(path_append, parameters)
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")
        
        if payload != None: 
            post_message  = payload
        else:
            post_message = self.payload
            self.trace("use loaded payload for post request")    

        request = requests.post(url, post_message, params=params, headers=self.headers, auth=auth)
        if request == None:
            self.status_code = 500
            self.error(f"request get failed: URL {url}")
        else:
            self.http_request = request
            self.status_code  = request.status_code    
        
        self.trace(f"request get result: {self.status_code}")    
        self.set_result_from_request()    
        return self.status_code

    def load_payload(self, filename:str) -> bool:
        try:
           self.payload = None
           self.payload = Path(filename).read_text()
           if self.payload != None:
            self.trace(f"request payload loaded from file {filename}")
            return True
           else:
            self.error(f"Error while loading payload from file {filename}")
            return False 
        except Exception as exc:
            self.error(f"Error while loading payload: {type(exc)} - {exc}")
            return False

class HTTPBackend(Backend):

    def __init__(self, name:str, url:str, auth:Auth=None):
        super().__init__(name, auth)
        self.type = "pydeen.HTTPBackend"
        self.set_property(Backend.BACKEND_PROP_URL, url)


class HTTPConnector(Connector):
    """
        Connector for HTTP Calls
    """
    def __init__(self, backend:Backend=None, url_or_endpoint:str="") -> None:
            
            # check backend 
            if backend == None:
                raise Exception("HTTP Connector via url not implemented yet")
                self.endpoint = ""    
                # if url_or_endpoint == "" or url_or_endpoint.find("://") < 1:
                #     raise Exception("invalid URL if no backend is given") 
                
                # split_protocol = url.split("://")
                # protocol = split_protocol[0]
                # rest_protocol = split_protocol[1]

                # pos_path = rest_protocol.find("/")
                # if pos_path > 0:
                #     hostname = rest_protocol.left(pos_path)
                #     path = rest_protocol.
            else:
                self.endpoint = url_or_endpoint
    
            Connector.__init__(self, backend)
            self.type = "pydeen.HTTPConnector"
            
    def path_append(self, path, append) -> str:
        if append == "" or append == None:
            return path
        if path == "":
            return append
        if path[-1] == "/" or append[0] == "/":
            return path + append
        else:
            return path + "/" + append

    def build_url(self, path_append, parameters:dict=None) -> str:
        # check url is given by backend
        url = self.get_backend().get_property(Backend.BACKEND_PROP_URL)
        if url == None or url == "":
        # no: build via backend fragments    
            result = self.get_backend().get_property(Backend.BACKEND_PROP_PROTOCOL) + "://"
            result += self.get_backend().get_property(Backend.BACKEND_PROP_HOST)
            port = self.get_backend().get_property(Backend.BACKEND_PROP_PORT)
            if port != None and port != "":
                result += ":" + port
        
            result = self.path_append(result, self.get_backend().get_property(Backend.BACKEND_PROP_PATH))
            result = self.path_append(result, self.endpoint)
            result = self.path_append(result, path_append)
        else:
        # yes: use this without further fragments except append info    
            result = self.path_append(url, path_append)

        # check for parameters
        if parameters != None:
            self.trace("build url with parameters detected")
            url_params = ''
            for name in parameters.keys():
                sep = "="
                if name == "$filter":
                    value = str(parameters[name]).lower()
                    if value.find("contains") >= 0:
                        self.trace(f"OData filter exception found for {value}")
                        sep = " "

                url_param = name + sep + parameters[name]
                if url_params == '':
                    url_params = url_param
                else:
                    url_params += '&' + url_param

            if result.find("?") < 0:
                result += "?" + url_params
            else:
                parts = result.split("?")
                result = parts[0] + '?' + parts[1] + '&' + url_params


        print("URL:", result)
        return result

    def create_request(self) -> HTTPRequest:
        request = HTTPRequest(self)   
        request.debug = self.debug   # forward debug mode 
        request.interactive = self.interactive
        return request   