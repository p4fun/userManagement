import webapp2
import uuid
import cgi
import json
import urllib2
from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
    id = ndb.StringProperty(required = True)
    firstName = ndb.StringProperty(required = True)
    middleName = ndb.StringProperty()
    lastName = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    messages = ndb.KeyProperty(kind='Message', repeated=True)

class Message(ndb.Model):
    id = ndb.StringProperty(required = True)
    fromUser = ndb.KeyProperty(kind='User')
    toUser = ndb.KeyProperty(kind='User')
    content = ndb.StringProperty(required = True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MessageHandler(webapp2.RequestHandler):
    def get(self):
	self.response.headers['Content-Type'] = 'application/json'
	data = {}
        messages = Message.query().order(Message.id)
        messageData = ''
        i = messages.count()
        j = 0
        for message in messages:
           print message.id
	   data['id'] = message.id
	   data['fromUser'] = message.fromUser.get().id
           data['toUser'] = message.toUser.get().id
           data['content'] = message.content
           j += 1
           if j != i:
           	messageData += json.dumps(data) + ","
           else:
		messageData += json.dumps(data)
        messageData = "[" + messageData + "]"
        self.response.out.write(messageData)
	
    def post(self):
	jsonstring = self.request.body
	jsonobject = json.loads(jsonstring)
	fromUserIdParam = jsonobject.get('fromId')
	toUserIdParam = jsonobject.get('toId')
	contentParam = jsonobject.get('message')
        fromUserKey = self.getUser(fromUserIdParam).key
	toUserKey = self.getUser(toUserIdParam).key
        message = Message(id=str(uuid.uuid1()),content=contentParam,fromUser=fromUserKey,toUser= toUserKey)
        newMessageKey = message.put()
        toUser = toUserKey.get()
        toUser.messages.append(newMessageKey)
        toUser.put()
  
    def getUser(self,userId):
	users = User.query().order(User.id)
	for user in users:
          if str(user.id)==userId:
		return user

    def delete(self):
	ndb.delete_multi(Message.query().fetch(keys_only=True)) 


class UserHTMLMsgHandler(webapp2.RequestHandler):
    def post(self):
	jsonstring = self.request.body
	jsonobject = json.loads(jsonstring)
	userId = jsonobject.get('id')
	users = User.query().order(User.id)
        messageData = ''
        for user in users:
          if str(user.id)==userId:
	    i = len(user.messages)
            j = 0
            for message in user.messages:
	      messageEntity = message.get()
	      messageData = 'id='+cgi.escape(messageEntity.id)+'|fromUser='+cgi.escape(messageEntity.fromUser.get().id)+"|content="+cgi.escape(messageEntity.content)     
      	      self.response.out.write('<blockquote>%s</blockquote>' % messageData)
"""
API to get user by id
"""
class UserHandler(webapp2.RequestHandler):

    def post(self):
	jsonstring = self.request.body
	jsonobject = json.loads(jsonstring)
	userId = jsonobject.get('id')
	users = User.query().order(User.id)
        userData = ''
        data = {}
        messageData = ''
	msg = {}
        for user in users:
          if str(user.id)==userId:
	    data['id'] = user.id
	    data['fname'] = user.firstName
	    data['mname'] = user.middleName
	    data['lname'] = user.lastName
	    data['email'] = user.email
	    data['password'] = user.password
            i = len(user.messages)
            print "i>>" + str(i)
            j = 0
            for message in user.messages:
                messageEntity = message.get()
		msg['fromUser'] = messageEntity.fromUser.get().id
		msg['content'] = messageEntity.content
		j += 1
           	if j != i:
           	  messageData += json.dumps(msg) + ","
           	else:
	          messageData += json.dumps(msg)
	    messageData = "[" + messageData + "]"
            data['messages'] = messageData
            userData = json.dumps(data)
	self.response.headers['Content-Type'] = 'application/json'
	self.response.out.write(userData)

class LoginHandler(webapp2.RequestHandler):
    def post(self):
        jsonstring = self.request.body
	jsonobject = json.loads(jsonstring)
	email = jsonobject.get('email')
        password = jsonobject.get('pass')
        data = {}
        user = self.findUserByEmailAndPassword(email,password)
        if user!=None:
	  data['id'] = user.id
	  data['name'] = user.firstName + " " + user.middleName + " " + user.lastName
	  data['email'] = email
	else:
	  data['id'] = data['name'] = data['email'] = None
	self.response.headers['Content-Type'] = 'application/json'
	self.response.out.write(json.dumps(data))

    def findUserByEmailAndPassword(self,emailParam,passwordParam):
	user = User.query(User.email == emailParam,User.password == passwordParam)
	if user!=None:
           return user.get()
        else:
           return None

class UserRegHandler(webapp2.RequestHandler):
     def get(self):
        users = User.query()
        for user in users:
           userData = 'id='+cgi.escape(user.id)+'|fname='+cgi.escape(user.firstName)+'|mname='+cgi.escape(user.middleName)
	   userData += '|lname='+cgi.escape(user.lastName)+'|email='+cgi.escape(user.email)+'|password='+cgi.escape(user.password)
      	   self.response.out.write('<blockquote>%s</blockquote>' % userData)


class UserRegistrationHandler(webapp2.RequestHandler):
    def post(self):
        jsonstring = self.request.body
	jsonobject = json.loads(jsonstring)
	firstNameParam = jsonobject.get('fname')
        middleNameParam = jsonobject.get('mname')
        lastNameParam = jsonobject.get('lname')
        emailParam = jsonobject.get('email')
        passwordParam = jsonobject.get('password')
        print 'fname='+firstNameParam+"/lname="+lastNameParam
        user = User(id=str(uuid.uuid1()),firstName=firstNameParam,middleName=middleNameParam,
	   lastName=lastNameParam,email=emailParam,password=passwordParam)
        user.put()
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
	data = {}
        users = User.query().order(User.id)
        userData = ''
        i = users.count()
        j = 0
        for user in users:
           print user.id
	   data['id'] = user.id
	   data['fname'] = user.firstName
           data['mname'] = user.middleName
           data['lname'] = user.lastName
           data['email'] = user.email
           data['password'] = user.password
           """data['messages'] = user.messages"""
           j += 1
           if j != i:
           	userData += json.dumps(data) + ","
           else:
		userData += json.dumps(data)
        userData = "[" + userData + "]"
        self.response.out.write(userData)

    def delete(self):
	ndb.delete_multi(User.query().fetch(keys_only=True)) 


app = webapp2.WSGIApplication([
    (r'/auth' , LoginHandler),
    (r'/users', UserRegistrationHandler),
    (r'/user', UserHandler),
    (r'/deleteUsers',UserRegistrationHandler),
    (r'/sendMessage',MessageHandler),
    (r'/usersHtml', UserRegHandler),
    (r'/messageHtml',UserHTMLMsgHandler),
])
