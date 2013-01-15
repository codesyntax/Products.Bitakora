## Script (Python) "tag"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

#$Id$

REQUEST = context.REQUEST

ts = REQUEST.get('traverse_subpath', '')

if len(ts) == 0:
    return context.tag_all_html(context, REQUEST)

else:
    REQUEST.set('id', ts[0])
    return context.tag_html(context, REQUEST)
