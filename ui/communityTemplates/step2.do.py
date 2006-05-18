## Script (Python) "step2.do"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
RESPONSE =  request.RESPONSE

ok_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
def validId(id):
    for letter in id:
        if letter not in ok_chars:
            return 0
    return 1

request.SESSION.set('title', request.form.get('title'))
request.SESSION.set('id', request.form.get('id'))

if container.get(request.form.get('id'), None) is not None:
    return RESPONSE.redirect('%s/step2?r=1' % context.communityUrl())
if not validId(request.form.get('id')):
    return RESPONSE.redirect('%s/step2?r=2' % context.communityUrl())  


return RESPONSE.redirect('%s/step3' % context.communityUrl())
