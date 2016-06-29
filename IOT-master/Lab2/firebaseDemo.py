from firebase import firebase
import json as simplejson
firebase = firebase.FirebaseApplication('https://brilliant-fire-6276.firebaseio.com',None)
result  = firebase.get('',None)
print result
 
name = {'Edison':10,'Pi':2016}
#data = json.dumps(name)
 
post = firebase.post('',name)
 
print post
