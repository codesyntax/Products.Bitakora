## Script (Python) "reminder.do"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
def generateKey(minlen=30, maxlen=40):
    """ """
    chars = 'abcdefghijkmnopqrstuvwxyz0123456789'
    key_chars=[]
    thislen = whrandom.choice(range(minlen,maxlen))
    for i in range(0,thislen):
        key_chars.append(whrandom.choice(chars))
    return "".join(key_chars)

def sendMail(email='',user='',key=''):
    """ """
    url = '%s/changepass?user=%s&key=%s' % (container.absolute_url(),user,key)
    mailhost=getattr(context,'MailHost')
    subject= context.gettext('Change password in %(communityname)s') % {'communityname': context.communityTitle()}
    body=context.gettext('To change password in %(communityname)s, go to this url:\n%(url)s') % {'communityname': context.communityTitle(), 'url': url}
    mailhost.simple_send(mto=email, mfrom='%s' % context.admin_mail, subject=subject, body=body)
    return 1

def validEmail(mail):
    if mail.find('@') != -1:
        s = mail.split('@')
        if len(s[0]) >= 1 and len(s[1]) >= 3 and s[1].find('.') != -1:
            return 1
    return 0

acl = getattr(context,'acl_users')
this_username=context.REQUEST.get('__ac_name','')

if acl.getUser(this_username):
    blog = context.usersBlog(this_username, blog=1)

    email = getattr(blog, 'contact_mail', '')

    if validEmail(email):
        key = generateKey()
        try:
            blog.manage_addProperty('key', key, 'string')
            sendMail(email=email,user=this_username,key=key)
            return context.REQUEST.RESPONSE.redirect('%s/reminder.done' % context.communityUrl())
        except:
            msg = context.gettext("There was an error reseting your password. Contact site admin for more details and provide your blog's url and your username")            

    else:
        #haven't email
        msg =  context.gettext('Oooooops! We haven\'t got your mail. Please, send an email to administrator at %s' % context.admin_mail)


else:
    #it doesn't exist
    msg = context.gettext('Oooooop.... this username is wrong')

return context.REQUEST.RESPONSE.redirect('%s/reminder?msg=%s' % (context.communityUrl(), msg))
