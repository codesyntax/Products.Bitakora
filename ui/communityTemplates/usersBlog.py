## Script (Python) "usersBlog"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user
##title=
##
cat = container.Catalog

blog = cat.searchResults(users=user)

if blog:
    return blog[0].getURL()

return ''

"""

for blog in container.objectValues('Squishblog'):
    if 'Blogger' in blog.get_local_roles_for_userid(user):
        return blog.absolute_url()

return ''
"""
