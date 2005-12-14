## Script (Python) "usersBlog"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user, blog=0
##title=
##
cat = container.Catalog

b = cat.searchResults(users=user)

if b:
    if not blog:
        return b[0].getURL()
    else:
        return b[0].getObject()

return ''

"""

for blog in container.objectValues('Squishblog'):
    if 'Blogger' in blog.get_local_roles_for_userid(user):
        return blog.absolute_url()

return ''
"""
