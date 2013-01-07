## Script (Python) "tag"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request=context.REQUEST
ts = request['traverse_subpath']

if len(ts)==0:
    return context.tag_all_html(context, request)

else:
    request.set('id',ts[0])
    return context.tag_html(context, request)
