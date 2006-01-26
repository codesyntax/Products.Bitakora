## Script (Python) "tagsAndPixels"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
tags = container.Catalog.uniqueValuesFor('tags')
zenbat = {}
for tag in tags:
    tagkop = container.Catalog.searchResults(tags=tag, meta_type='Post')
    zenbat[tag] = len(tagkop)

maxpx = 2.00
minpx = 0.70
difpx = maxpx-minpx

if zenbat.values():
    maxnum = max(zenbat.values())
    minnum = max(zenbat.values())

else:
    maxnum = 0
    minnum = 0

hiz = {}
for k,v in zenbat.items():
    hiz[k] = float(difpx*v/maxnum)+minpx

return hiz
