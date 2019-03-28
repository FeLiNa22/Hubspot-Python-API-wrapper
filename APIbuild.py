import requests
import json
import logging

class APIbuilder:
        
######################################################
######################################################
    
    def __init__(self,api):
        self.API = api
        self.portalID = self.getPortalId()
        self.logger = logging.getLogger('APIlog')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('APIlog.log')
        fh.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)
    
    def getPortalId(self):
        URL = 'https://api.hubapi.com/integrations/v1/me?hapikey='+self.API
        r=requests.get(URL)
        a = r.json()
        return (a['portalId'])

    def checkKey(self,dict,key,getValue=False): 
        if key in dict.keys(): 
            if getValue:
                return dict[key]
            else:
                return True
        else: 
            return False
        
    def checkUsage(self):
       URL = 'https://api.hubapi.com/integrations/v1/limit/daily?hapikey='+self.API
       r=requests.get(URL)
       a = r.json()
       print(a)
######################################################
######################################################
    
    def Forms(self,function,call,args):
        if 'create' in function.lower() :
            return self.createForm(call,args)
        elif 'get' in function.lower() :
            return self.getForm(call,args)
        elif 'update' in function.lower() :
            return self.updateForm(call,args)
        elif 'submit' in function.lower() :
            return self.submitForm(call,args)
    
    def submitForm(self,call,args):
        if 'byid' in call.lower():
            return self.submitFormbyID(args)
######################################################
######################################################
    
    def Owners(self,function,call,args):
        if 'create' in function.lower() :
            return self.createOwner(call,args)
        elif 'get' in function.lower() :
            return self.getOwner(call,args)
        elif 'update' in function.lower() :
            return self.updateOwner(call,args)
    
    def getOwner(self,call,args):
        if 'byemail' in call.lower():
            return self.getOwnerbyEmail(args)

######################################################
######################################################
    
    def Companies(self,function,call,args):
        if 'create' in function.lower() :
            return self.createCompany(call,args)
        elif 'get' in function.lower() :
            return self.getCompany(call,args)
        elif 'update' in function.lower() :
            return self.updateCompany(call,args)
    
    def getCompany(self,call,args):
        if 'all' in call.lower():
            return self.getAllCompanies(args)
        if 'recent' in call.lower():
            return self.getRecentCompanies(args)
   
    def updateCompany(self,call,args):
        if 'inbatch' in call.lower():
            return self.updateCompanyinBatch(args)
        
######################################################
######################################################
    
    def Contacts(self,function,call,args):
        if 'create' in function.lower() :
            return self.createContact(call,args)
        elif 'get' in function.lower() :
            return self.getContact(call,args)
        elif 'update' in function.lower() :
            return self.updateContact(call,args)
        elif 'merge' in function.lower():
             return self.mergeContact(call,args)
         
    def createContact(self,call,args):
        return
    
    def mergeContact(self,call,args):
        if 'byid' in call.lower():
            return self.mergeContactsbyID(args)
        
    def getContact(self,call,args):
        if 'recent' in call.lower():
            return self.getRecentContacts(args)
        elif 'all' in call.lower():
            return self.getAllContacts(args)
        elif 'byemail' in call.lower():
            return self.getContactbyEmail(args)
    
    def updateContact(self,call,args):
        if 'byemail' in call.lower():
            return self.updateContactbyEmail(args)
        elif 'byid' in call.lower():
            return self.updateContactbyID(args)
        elif 'inbatch' in call.lower():
            return self.updateContactinBatch(args)
        
######################################################
######################################################
   
    def Engagements(self,function,call,args):
        if 'create' in function.lower() :
            return self.createEngagement(call,args)
        elif 'get' in function.lower() :
            return self.getEngagement(call,args)
        elif 'update' in function.lower() :
            return self.updateEngagement(call,args)

    def createEngagement(self,call,args):
        if 'note' in call.lower():
            return self.createNote(args)
        elif 'email' in call.lower():
            return self.createEmail(args)
        elif 'task' in call.lower():
            return self.createTask(args)
        elif 'call' in call.lower():
            return self.createNote(args)
        elif 'meeting' in call.lower():
            return self.createMeeting(args)
    
    def getEngagement(self,call,args):
        if 'all' in call.lower():
            return self.getAllEngagements(args)

    def updateEngagement(self,call,args):
            return 
    
######################################################
######################################################

    
#########################################################################################################################
#                                                   MERGE FUNCTIONS                                                    #
#########################################################################################################################
    def mergeContactsbyID(self,args):
        # args = {'Main ID': 234324234, 'Secondary IDs':3219887218}
        if self.checkKey(args,'Main ID') :
            main_contact= args['Main ID']
        if self.checkKey(args,'Secondary ID'):
            secondary_contact= args['Secondary ID']
        URL = 'https://api.hubapi.com/contacts/v1/contact/merge-vids/'+str(main_contact)+'/?hapikey='+self.API
        headers = {'content-type':'application/json'}
        Engagement = {'vidToMerge': secondary_contact}
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        if r.status_code == 200:
            return r
        else:
            self.logger.error('Could not Merge '+str(main_contact) +' With '+ str(secondary_contact))
#########################################################################################################################
#                                                   SUBMIT FUNCTIONS                                                    #
######################################################################################################################### 

    def submitFormbyID(self,args):
        options = ''
        if self.checkKey(args,'Context'):
            options += '&hs_context=' + json.dumps(args['Context'])
        if self.checkKey(args,'Email'):
            options += '&email='+args['Email']
        if self.checkKey(args,'Properties') and self.checkKey(args,'Values'):
            Properties = args['Properties']
            Values = args['Values']
            for i in range(len(Properties)):
                options += '&'+Properties[i]+'='+str(Values[i])
        formID = self.checkKey(args,'ID',getValue=True)
        URL = 'https://forms.hubspot.com/uploads/form/v2/'+str(self.portalID)+'/'+str(formID)+ '?'+options
        headers = {'content-type':'application/x-www-form-urlencoded'}
        r = requests.post(URL, headers= headers)
        return r

#########################################################################################################################
#                                                   UPDATE FUNCTIONS                                                    #
######################################################################################################################### 
            
    def updateContactbyEmail(self,args):
        if self.checkKey(args,'Email'):
            Email = args['Email']
        if self.checkKey(args,'Property'):
            Property = args['Property']
        if self.checkKey(args,'Value'):
            Value = args['Value']
        URL = 'https://api.hubapi.com/contacts/v1/contact/email/'+Email+'/profile?hapikey='+self.API
        headers = {'content-type':'text/html'}
        Engagement = {"properties": [{"property": Property,"value": Value}]}
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return r
    
    def updateContactbyID(self,args):
        props=[]
        if self.checkKey(args,'Properties') and self.checkKey(args,'Values'):
            Properties = args['Properties']
            Values = args['Values']
            for i in range(len(Properties)):
                props.append( {"property": Properties[i] , "value": Values[i]} ) 
        if self.checkKey(args,'ID'):
            ID = args['ID']
        Engagement=( {"properties": props } )
        URL = 'https://api.hubapi.com/contacts/v1/contact/vid/'+str(ID)+'/profile?hapikey='+self.API
        headers = {'content-type':'application/json'}
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return r
    
    def updateContactinBatch(self,args):
        Engagement =[]
        for contact in args:
            props=[]
            if self.checkKey(contact,'Properties') and self.checkKey(contact,'Values'):
                Properties = contact['Properties']
                Values = contact['Values']
                for i in range(len(Properties)):
                    props.append( {"property": Properties[i] , "value": Values[i]} ) 
            if self.checkKey(contact,'ID'):
                ID = contact['ID']
                Engagement.append( { "vid" : ID , "properties": props } )
            if self.checkKey(contact,'Email'):
                Email = contact['Email']
                Engagement.append( { "email" : Email, "properties": props } )
        URL = 'https://api.hubapi.com/contacts/v1/contact/batch/?hapikey='+self.API
        headers = {'content-type':'application/json'}
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return r
    
    
    def updateCompanyinBatch(self,args):
        Engagement =[]
        for company in args:
            props=[]
            if self.checkKey(company,'Properties') and self.checkKey(company,'Values'):
                Properties = company['Properties']
                Values = company['Values']
                for i in range(len(Properties)):
                    props.append( {"name": Properties[i] , "value": Values[i]} ) 
            if self.checkKey(company,'ID'):
                ID = company['ID']
                Engagement.append( { "objectId" : ID , "properties": props } )
        URL = 'https://api.hubapi.com/companies/v1/batch-async/update?hapikey='+self.API
        headers = {'content-type':'application/json'}
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return r
   
#########################################################################################################################
#                                                   GET FUNCTIONS                                                       #
#########################################################################################################################        
    def getAllCompanies(self,args):
        options=''
        if self.checkKey(args,'Properties'):
            for prop in args['Properties']:
                options += '&properties='+str(prop)
        if self.checkKey(args,'Count'):
            options += '&limit='+str(args['Count'])
        if self.checkKey(args,'Offset'):
            options += '&offset='+str(args['Offset'])
        URL = 'https://api.hubapi.com/companies/v2/companies/paged?hapikey='+self.API + options
        r=requests.get(URL)
        a = r.json()
        return a       
    
    
    def getAllContacts(self,args):
        options=''
        if self.checkKey(args,'Properties'):
            for prop in args['Properties']:
                options += '&property='+str(prop)
        if self.checkKey(args,'Count'):
            options += '&count='+str(args['Count'])
        if self.checkKey(args,'Offset'):
            options += '&vidOffset='+str(args['Offset'])
        URL = 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all?hapikey='+self.API + options
        r=requests.get(URL)
        a = r.json()
        return a           
    
    def getAllEngagements(self,args):
        options=''
        if self.checkKey(args,'Properties'):
            for prop in args['Properties']:
                options += '&property='+str(prop)
        if self.checkKey(args,'Count'):
            options += '&limit='+str(args['Count'])
        if self.checkKey(args,'Offset'):
            options += '&Offset='+str(args['Offset'])
        URL = 'https://api.hubapi.com/engagements/v1/engagements/paged?hapikey='+self.API+options
        r=requests.get(URL)
        a = r.json()
        return a     
    
    def getOwnerbyEmail(self,args):
        options=''
        if self.checkKey(args,'Email'):
            options += '&email='+args['Email']
        URL = 'https://api.hubapi.com/owners/v2/owners?hapikey='+self.API+options
        r=requests.get(URL)
        a = r.json()
        return a
        
    def getContactbyEmail(self,args):
        if self.checkKey(args,'Email'):
            Email = args['Email']
        URL = 'https://api.hubapi.com/contacts/v1/contact/email/'+Email+'/profile?hapikey='+self.API
        r=requests.get(URL)
        a = r.json()
        return a
   
    def getRecentContacts(self,args):
        options=''
        firstPull = self.checkKey(args,'FirstPull',getValue=True)
        if self.checkKey(args,'Count'):
            options += '&count='+str(args['Count'])
        if self.checkKey(args,'Properties'):
            for prop in args['Properties']:
                options += '&property='+str(prop)
        if firstPull==False:
            if self.checkKey(args,'Offset'):
                options += '&vidOffset='+str(args['Offset'])
            if self.checkKey(args,'Time'):
                options += '&timeOffset='+str(args['Time'])
        URL = 'https://api.hubapi.com/contacts/v1/lists/recently_updated/contacts/recent?hapikey='+self.API +options
        r=requests.get(URL)
        ##Validation of error
        if r.status_code==200:
            return r.json()
        else:
            self.getRecentContacts(args)
   
    def getRecentCompanies(self,args):
        options=''
        if self.checkKey(args,'Count'):
            options += '&count='+str(args['Count'])
        if self.checkKey(args,'Offset'):
            options += '&offset='+str(args['Offset'])
        URL = 'https://api.hubapi.com/companies/v2/companies/recent/modified?hapikey='+self.API +options
        r=requests.get(URL)
        a = r.json()
        return a
                
    def createNote(self,args):
        if self.checkKey(args,'engagementID'):
            engagementID = args['engagementID']
        if self.checkKey(args,'ownerID'):
            ownerID = args['ownerID']
        if self.checkKey(args,'contactID'):
            contactID = args['contactID']
        if self.checkKey(args,'timestamp'):
            timestamp = args['timestamp']
        if self.checkKey(args,'text'):
            text = args['text']
        URL ='https://api.hubapi.com/engagements/v1/engagements?hapikey='+self.API
        headers = {'content-type':'application/json'}
        Engagement = {
          "engagement": {"type": "NOTE","id": engagementID,"portalId": self.portalID,"active": True,"ownerId": ownerID,"timestamp": timestamp*1000},
          "associations": {"contactIds": [contactID],"companyIds": [],"dealIds": [],"ownerIds": [],"workflowIds": [], "ticketIds": []},
          "attachments": [],
          "metadata": {"body": text}
                      }
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return (r.content)
        
    def createTask(self,args):
        if self.checkKey(args,'engagementID'):
            engagementID = args['engagementID']
            
        if self.checkKey(args,'contactID'):
            contactID = args['contactID']
            
        if self.checkKey(args,'ownerID'):
            ownerID = args['ownerID']
            
        if self.checkKey(args,'timestamp'):
            timestamp = args['timestamp']
            
        if self.checkKey(args,'title'):
            title = args['title']
            
        if self.checkKey(args,'status'):
            status = args['status']
            
        if self.checkKey(args,'body'):
            body = args['body']
            
        if self.checkKey(args,'objtype'):
            objtype = args['objtype']

            
        URL ='https://api.hubapi.com/engagements/v1/engagements?hapikey='+self.API
        headers = {'content-type':'application/json'}
        
        Engagement = {
          "engagement": {
            "type": "TASK",
            "id": engagementID,
            "portalId": self.portalID,
            "active": True,
            "ownerId": ownerID,
            "timestamp": timestamp*1000
          },
          "associations": {
            "contactIds": [contactID],
            "companyIds": [],
            "dealIds": [],
            "ownerIds": [],
            "workflowIds": [],
            "ticketIds": []
          },
          "attachments": [],
          
          "metadata": {
            "body": body,
            "subject": title,
            "status": status,
            "forObjectType": objtype
          }
          
        }
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return (r.content)
    
    def createMeeting(self,args):
        if self.checkKey(args,'engagementID'):
            engagementID = args['engagementID']
        if self.checkKey(args,'contactID'):
            contactID = args['contactID']
        if self.checkKey(args,'ownerID'):
            ownerID = args['ownerID']
        if self.checkKey(args,'timestamp'):
            timestamp = args['timestamp']
        if self.checkKey(args,'title'):
            title = args['title']
        if self.checkKey(args,'startTime'):
            startTime = args['startTime']
        if self.checkKey(args,'endTime'):
            endTime = args['endTime']
        if self.checkKey(args,'body'):
            body = args['body']
        URL ='https://api.hubapi.com/engagements/v1/engagements?hapikey='+self.API
        headers = {'content-type':'application/json'}
        Engagement = { 
          "engagement": {"type": "MEETING","id": engagementID,"portalId": self.portalID,"active": True,"ownerId": ownerID,"timestamp": timestamp*1000},
          "associations": {"contactIds": [contactID],"companyIds": [],"dealIds": [],"ownerIds": [],"workflowIds": [],"ticketIds": []},
          "attachments": [],
          "metadata": {"body": body,"startTime": startTime,"endTime": endTime,"title": title}
                      }
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return (r.content)

    def createCall(self,args, engagementID, contactID, ownerID, timestamp, toNumber, fromNumber, status, duration, recordingURl ):
        if self.checkKey(args,'engagementID'):
            engagementID = args['engagementID']
            
        if self.checkKey(args,'contactID'):
            contactID = args['contactID']
            
        if self.checkKey(args,'ownerID'):
            ownerID = args['ownerID']
            
        if self.checkKey(args,'timestamp'):
            timestamp = args['timestamp']
            
        if self.checkKey(args,'body'):
            body = args['body']
            
        if self.checkKey(args,'toNumber'):
            toNumber = args['toNumber']
            
        if self.checkKey(args,'fromNumber'):
            fromNumber = args['fromNumber']
            
        if self.checkKey(args,'status'):
            status = args['status']
            
        if self.checkKey(args,'duration'):
            duration = args['duration']
            
        if self.checkKey(args,'recordingURl'):
            recordingURl = args['recordingURl']
        
        URL ='https://api.hubapi.com/engagements/v1/engagements?hapikey='+self.API
        headers = {'content-type':'application/json'}
        
        Engagement = {
          "engagement": {
            "type": "CALL",
            "id": engagementID,
            "portalId": self.portalID,
            "active": True,
            "ownerId": ownerID,
            "timestamp": timestamp*1000
          },
          "associations": {
            "contactIds": [contactID],
            "companyIds": [],
            "dealIds": [],
            "ownerIds": [],
            "workflowIds": [],
            "ticketIds": []
          },
          "attachments": [],
          
          "metadata" : {
            "toNumber" : toNumber,
            "fromNumber" : fromNumber,
            "status" : status,
            "durationMilliseconds" : duration,
            "recordingUrl" : recordingURl,
            "body" : body
            }     
          
        }
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return (r.content)



    def createEmail(self,args):
        if self.checkKey(args,'engagementID'):
            engagementID = args['engagementID']
            
        if self.checkKey(args,'contactID'):
            contactID = args['contactID']
            
        if self.checkKey(args,'ownerID'):
            ownerID = args['ownerID']
            
        if self.checkKey(args,'timestamp'):
            timestamp = args['timestamp']
            
        if self.checkKey(args,'sender_email'):
            sender_email = args['sender_email']
            
        if self.checkKey(args,'sender_firstname'):
            sender_firstname = args['sender_firstname']
            
        if self.checkKey(args,'sender_lastname'):
            sender_lastname = args['sender_lastname']
            
        if self.checkKey(args,'client_email'):
            client_email = args['client_email']
            
        if self.checkKey(args,'client_firstname'):
            client_firstname = args['client_firstname']
            
        if self.checkKey(args,'client_lastname'):
            client_lastname = args['client_lastname']
            
        if self.checkKey(args,'subject'):
            subject = args['subject']
            
        if self.checkKey(args,'body'):
            body = args['body']
        
        URL ='https://api.hubapi.com/engagements/v1/engagements?hapikey='+self.API
        headers = {'content-type':'application/json'}
        
        Engagement = {
          "engagement": {
            "type": "EMAIL",
            "id": engagementID,
            "portalId": self.portalID,
            "active": True,
            'ownerId' : ownerID,
            'timestamp': timestamp*1000
          },
          "associations": {
            "contactIds": [contactID],
            "companyIds": [],
            "dealIds": [],
            "ownerIds": [],
            "workflowIds": [],
            "ticketIds": []
          },
          "attachments": [],

          "metadata": {
            "from": {
              "email": sender_email,
              "firstName": sender_firstname,
              "lastName": sender_lastname
            },
            "to": [
              {
                "email":client_firstname+" "+client_lastname+" <"+client_email+">",
              }
            ],
            "cc": [],
            "bcc": [],
            "subject": subject,
            "text": body
            }
        }
        r = requests.post(URL, data = json.dumps(Engagement), headers= headers)
        return (r.content)
          
        
        
        
#EXAMPLES using my fake acc
#API = 'b7f02e14-9c35-4dcb-976e-fa0de91944d9'
#pkg = APIbuilder(API)

#print(pkg.Contacts('get','all',{'Count':100,'Offset':0,'Properties':['Email']}))

#pkg.createNoteEngagement( engagementID = 328550660, contactID = 101, ownerID = 1, createdAt = 1549380058, lastUpdated = 1549380058, timestamp = 1559380716, text = 'Ayyt we gucci')
#print(pkg.UpdateContactProperties(Email = 'lol@gmail.com', Property = 'firstname', Value = 'hellomate'))


#print(pkg.getOwnerIDbyEmail('raulpatel97@gmail.com'))
#contactid = pkg.getContactIDbyEmail('lol@gmail.com')


#print(pkg.createEmailEngagement(engagementID=1234356789 ,contactID=int(contactid), timestamp=1565218117, sender_email= 'me45@gmail.com' ,sender_firstname = 'Raul',sender_lastname='Patel', client_email= 'lol@gmail.com', client_firstname='hellomate',client_lastname='lel' ,subject = 'Final Tests', text = 'I cba anymore\n\n time to commit so is ur mama'))
#print(pkg.getEngagements())



## My API - 97dfa9cc-5b2f-446b-99e9-4dd417057853
## COMPANIES - b7f02e14-9c35-4dcb-976e-fa0de91944d9
