## Script (Python) "changepass.do"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

request = context.REQUEST
pass1 =request.get('password','1')
pass2 =request.get('password_confirm','2')
username=request.get('__ac_name','')
req_key=request.get('key','')
roles=[]
domains=''

acl = getattr(context,'acl_users')
blog = context.usersBlog(username, blog=1)
original_key = blog.getProperty('key', '')

if original_key and original_key==req_key and pass1==pass2:
    acl.userFolderEditUser(username, pass1, roles, domains)
    blog.manage_delProperties(['key'])
    return context.REQUEST.RESPONSE.redirect('/login_form?msg=%s' % context.gettext('Your password has been changed'))
elif pass1!=pass2:
    return context.REQUEST.RESPONSE.redirect('/changepass?user=%s&key=%s&msg=%s' % (username,req_key,'password1 != password2'))
elif (not original_key) or original_key!=req_key:
    return context.REQUEST.RESPONSE.redirect('/changepass?user=%s&key=%s&msg=%s' % (username,req_key,'Wrong key'))

return context.REQUEST.RESPONSE.redirect('changepass?user=%s&key=%s' % (username,req_key,))
