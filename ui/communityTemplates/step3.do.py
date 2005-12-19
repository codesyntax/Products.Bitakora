## Script (Python) "step3.do"
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

username = request.SESSION.get('username')
password = request.SESSION.get('password')
contact_mail = request.SESSION.get('contact_mail')
title = request.SESSION.get('title')
id = request.SESSION.get('id')
template = str(request.get('template'))

# create the blog
container.manage_addProduct['Bitakora'].manage_addBitakora(str(id), title, u'', contact_mail)

blog = container.get(id)

# add the user
container.acl_users.userFolderAddUser(username, password, roles=[], domains=[])
blog.manage_addLocalRoles(username, ['Blogger'])

# clear the session object
request.SESSION.clear()

blog.select_template(template)

container.Catalog.catalog_object(blog, '/'.join(blog.getPhysicalPath()))

# We are done !!!!
RESPONSE.redirect('%s/step3.done' % context.communityUrl())
