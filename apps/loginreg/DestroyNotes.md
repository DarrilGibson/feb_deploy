Destroy

HTML calls with this
<td><a href="/wishlist/{{wish.id}}/delete">Remove from my Wishlist</a></td>

URLs.py sees it with this:
url(r'^(?P<id>\d+)/delete$', views.destroy, name="destroy"),

Views.py handles it with this

def destroy(request, id):
    print "in destroy"
    action = Wishlist.objects.deleteitem(id)

  models.py destroys it with this

  def deleteitem (self, id):
    print "in models:deleteitem"
    action = self.get(id=id)
    action.delete()
    print "action"
    print action
    return(True)
