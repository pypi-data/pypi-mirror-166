import requests
class openioe_apis:
    def __init__(self, *args):
        self.UserIDPinAPIKeys=[]
        self.response_text=[]
        self.response_status_code=[]  
        self.endpoint='http://gnanodaya.org:8080/openioe/api/'
        if len(args) == 0:
            self.a=0           
        elif len(args) == 1:
            self.a=args[0]
        
    def ReadAPI(self, *args):
        if len(args) == 0:
            for i in range(len(self.UserIDPinAPIKeys)):
                print(self.endpoint+'read/'+self.UserIDPinAPIKeys[i][2]+'/'+self.UserIDPinAPIKeys[i][0]+'/'+self.UserIDPinAPIKeys[i][1]+'/')
                resp = requests.get(self.endpoint+'read/'+self.UserIDPinAPIKeys[i][2]+'/'+self.UserIDPinAPIKeys[i][0]+'/'+self.UserIDPinAPIKeys[i][1]+'/')
                self.response_text[i]=list(resp.text)
                self.response_status_code[i]=resp.status_code
        else:
            print('Do not Pass parameters')
            
            
    def WriteAPI(self, *args):
        if len(args) == 0:
            for i in range(len(self.UserIDPinAPIKeys)):
                print(self.endpoint+'read/'+self.UserIDPinAPIKeys[i][2]+'/'+self.UserIDPinAPIKeys[i][0]+'/'+self.UserIDPinAPIKeys[i][1]+'/')
                resp = requests.get(self.endpoint+'read/'+self.UserIDPinAPIKeys[i][2]+'/'+self.UserIDPinAPIKeys[i][0]+'/'+self.UserIDPinAPIKeys[i][1]+'/')
                self.response_text[i]=list(resp.text)
                self.response_status_code[i]=resp.status_code
        else:
            print('Do not Pass parameters')

        
            
    