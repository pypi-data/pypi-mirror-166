import requests 
from collections import OrderedDict


__author__ = "SMS-iT: QoS"


class smsit:
    '''
    Class for wrapping up sms-it endpoints so that they can be used directly.

    Available Methods: 'addAppointment', 'addContact', 'checkCredits', 'generateOTP', 'getContact', 'getContactByName', 'getGroupsList', 'name', 'sendMessageToContacts', 'sendMessageToGroup', 'token', 'validateOTP'

    '''

    def __init__(self, token,version):
        self.name = "smsit wrapper"
        self.version = version 
        self.token = token
        versions = ['cloud', 'decentral']
        if self.version not in versions:
            print('\nVersion is wrong!')
            return "Version is to be: cloud or decentral"



    def sendMessageToGroup(self,number,groupname,message):

        if self.version == 'cloud':
            url = f"https://controlpanel.smsit.ai/apis/smsgroup/?apikey={self.token}&from={number}&to={groupname}&message={message}"

        if self.version == "decentral":
            url = f"https://decontrolpanel.smsit.ai/apis/smsgroup/?apikey={self.token}&from={number}&to={groupname}&message={message}"

        r = requests.get(url)
        data = r.json()
        return data
    
    def sendMessageToContacts(self,number,contactnumber,message,bulk=False):
        if bulk == False:
            if self.version == 'cloud':
                url = f"https://controlpanel.smsit.ai/apis/smscontact/?apikey={self.token}&from={number}&to={contactnumber}&message={message}"

            if self.version == "decentral":
                url = f"https://decontrolpanel.smsit.ai/apis/smscontact/?apikey={self.token}&from={number}&to={contactnumber}&message={message}"
            r = requests.get(url)
            data = r.json()
            return data
        else:
            if(type(contactnumber) == list):
                contact = ""
                for i in range(len(contactnumber)):
                    if i == len(contactnumber):
                        contact+=f"{contactnumber[i]}"
                    else:
                        contact+=f"{contactnumber[i]},"
                r = requests.get(url)
                data = r.json()
                return data
            
            else:
                return "for bulk sending, the contact must be list"
    #get group list for cloud token
    #Shows only groups that are visible

    def getContactByName(self,name):
        if self.version == 'cloud':
            url = f"https://controlpanel.smsit.ai/apis/getcontacts/?apikey={self.token}&name={name}"

        if self.version == "decentral":
            url = f"https://decontrolpanel.smsit.ai/apis/getcontacts/?apikey={self.token}&name={name}"
        r = requests.get(url)
        data = r.json()
        return data
    
    #you can filter contacts based on relevant detailss
    def getContact(self,data):
        if self.version == 'cloud':
            url = f"https://controlpanel.smsit.ai/apis/getcontacts/?apikey={self.token}"

        if self.version == "decentral":
            url = f"https://decontrolpanel.smsit.ai/apis/getcontacts/?apikey={self.token}"

        if 'name' in data:
            url +=f"&name={data['name']}"
        if 'email' in data:
            url+=f"&email={data['email']}"
        if 'number' in data:
            url +=f"&name={data['number']}"
        if 'group' in data:
            url+=f"&email={data['group']}"
       
        
        #print(url)
        r = requests.get(url)
        data = r.json()
        return data



    def getGroupsList(self):

        if self.version == 'cloud':
            url = "https://controlpanel.smsit.ai/apis/getcontacts/"

        if self.version == "decentral":
            url = "https://decontrolpanel.smsit.ai/apis/getcontacts/"
            
        try:
            payload = {
                "apikey": f"{self.token}"
            }
            data =  OrderedDict(payload)
            #return data
            response = requests.post(url, data=data)
            data = response.json()
            if data['status'] == '-1':
                return "-1"

            ls = []
            #print(data['contacts'][1])
            for i in data['contacts']:
                ls.append(i['group'])

            myset = set(ls)
            #print(myset)
            return list(myset) 
        except Exception as e:
            print("Get group exception: ", e)
            return []


    #add a contacct to a group
    def addContact(self,groupname,data):
        '''
        The data is to be a dict type with keys number,email and name
        '''
        if self.version == 'cloud':

            url = f"https://controlpanel.smsit.ai/apis/addcontact/?apikey={self.token}&group={groupname}&number={data['number']}"
        if self.version == 'decenral':
            url = f"https://decontrolpanel.smsit.ai/apis/addcontact/apikey={self.token}&group={groupname}&number={data['number']}"
            

        if 'inputName' in data:
            url +=f"&name={data['name']}"
        if 'inputEmail' in data:
            url+=f"&email={data['email']}"

        r = requests.get(url)
        data = r.json()
        return data
        #if data["status"] == '-1':
        #    return -1 
        #return data


    #cgheck credits in the account 1 form sms 2 for voice/contacts/index
    def checkCredits(self,type):
        if self.version == 'cloud':
            url = f"https://controlpanel.smsit.ai/apis/getcreditbalance/?apikey={self.token}&type={type}"
        if self.version == 'decenral':
            url = f"https://decontrolpanel.smsit.ai/apis/getcreditbalance/?apikey={self.token}&type={type}"

        r = requests.get(url)
        data = r.json()
        return data

    #add appointment 
    def addAppointment(self,data):
        if self.version == 'cloud':

            url = f"https://controlpanel.smsit.ai/apis/addappointment/?apikey={self.token}&number={data['number']}&apptdate={data['date']}&status={data['status']}"
        if self.version == 'decenral':
            url = f"https://decontrolpanel.smsit.ai/apis/addappointment/?apikey={self.token}&number={data['number']}&apptdate={data['date']}&status={data['status']}"

        r = requests.get(url)
        data = r.json()
        return data


    def generateOTP(self):
        if self.version == 'cloud':

            url = f"https://controlpanel.smsit.ai/apis/generateOTP/?apikey={self.token}"
        if self.version == 'decenral':
            url = f"https://decontrolpanel.smsit.ai/apis/generateOTP/?apikey={self.token}"
        
        r = requests.get(url)
        data = r.json()
        return data


    #verify the previously generated otp (check generate otp function)
    def validateOTP(self,otp):
        if self.version == 'cloud':

            url = f"https://controlpanel.smsit.ai/apis/validateOtp/?apikey={self.token}&otp={otp}"
        if self.version == 'decenral':
            url = f"https://decontrolpanel.smsit.ai/apis/validateOtp/?apikey={self.token}&otp={otp}"
        
        r = requests.get(url)
        data = r.json()
        return data

