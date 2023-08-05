class openioe_apis:
    def __init__(self, *args):
        self.UserIDPinAPIKeys=[]
        self.response_text=[]
        self.response_status_code=[]  
        self.endpoint='http://gnanodaya.org:8080/openioe/api/'
        self.Data=[]
        if len(args) == 0:
            self.a=0           
        elif len(args) == 1:
            self.a=args[0]
            
    def Developer(self, *args):
        print('Hi, Welcome to OpenIoE')
        print('Developed by Dr. Venkataswamy R')
        print('https://venkataswamy.in')
        print('venkataswamy.r@gmail.com')
        
    def ReadAPI(self, *args):
        import requests
        if len(args) == 0:
            for i in range(len(self.UserIDPinAPIKeys)):
                u=self.endpoint+'showvalue/'+str(self.UserIDPinAPIKeys[i][0])+'/'+str(self.UserIDPinAPIKeys[i][1])+'/'
                resp = requests.get(u)
                self.response_text.append(resp.text)
                self.response_status_code.append(resp.status_code)
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
            
            
    def WriteAPI(self, *args):
        import requests
        if len(args) == 0:
            for i in range(len(self.UserIDPinAPIKeys)):
                u=self.endpoint+'updatevalue/'+str(self.UserIDPinAPIKeys[i][0])+'/'+str(self.UserIDPinAPIKeys[i][1])+'/'+str(self.Data[i])
                resp = requests.get(u)
                self.response_text.append(resp.text)
                self.response_status_code.append(resp.status_code)
        else:
            print('Do not Pass parameters')
        return self.response_text, self.response_status_code
        
            
    