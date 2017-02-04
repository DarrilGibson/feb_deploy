add wish item to another user

HTML calls with this
<td><a href="/wishlist/{{wish.id}}/addother">Remove from my Wishlist</a></td>

URLs.py sees it with this:
url(r'^(?P<id>\d+)/addother$', views.addother, name="addother"),

Views.py handles it with this

def destroy(request, id):
    get item objects
    get item name from item id
    add item name to current user
