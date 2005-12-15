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

request.SESSION.set('title', request.form.get('title'))
request.SESSION.set('id', request.form.get('id'))

if container.get(request.form.get('id'), None) is not None:
    return RESPONSE.redirect('%s/step2?r=4' % context.communityUrl())

return RESPONSE.redirect('%s/step3' % context.communityUrl())
