## Script (Python) "step1.do"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
def validEmail(mail):
    if mail.find('@') != -1:
        s = mail.split('@')
        if len(s[0]) >= 1 and len(s[1]) >= 3 and s[1].find('.') != -1:
            return 1
    return 0

request = container.REQUEST
RESPONSE =  request.RESPONSE

request.SESSION.set('username', request.form.get('username'))
request.SESSION.set('contact_mail', request.form.get('contact_mail'))

if request.form.get('password') != request.form.get('password2'):
    return RESPONSE.redirect('%s/step1?r=1' % self.communityUrl())
if request.form.get('username') in container.acl_users.getUserNames():
    return RESPONSE.redirect('%s/step1?r=2' % self.communityUrl())
if not validEmail(request.form.get('contact_mail')):
    return RESPONSE.redirect('%s/step1?r=3' % self.communityUrl())

request.SESSION.set('password', request.form.get('password'))

return RESPONSE.redirect('%s/step2' % self.communityUrl())
