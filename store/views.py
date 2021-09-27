# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Album, Artist, Contact, Booking
# Create your views here.


def index(request):
    all_albums = Album.objects.filter(
        available=True).order_by('created_at')[:12]
    albums = ["<li>{}</li>".format(album.title) for album in all_albums]
    # message = """<ul>{}</ul>""".format("\n".join(albums))
    template = loader.get_template('store/index.html')
    return HttpResponse(template.render(request=request))


def listing(request):
    all_albums = Album.objects.filter(
        available=True)
    albums = ["<li>{}</li>".format(album.title) for album in all_albums]
    message = """<ul>{}</ul>""".format("\n".join(albums))
    return HttpResponse(message)


def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(
        album.title, artists)
    return HttpResponse(message)


def search(request):
    query = request.GET.get('query')

    if not query:
        # Getting all albums if no query
        albums = Album.objects.all()
    else:
        # Looking into albums title if query
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        # Looking into album's artist if no result in albums
        albums = Album.objects.filter(artists__name__icontains=query)
    if not albums.exists():
        # If no results found in artists or albums
        message = "Aïe, nous n'avons trouvé aucun résultat"
    else:
        albums = ["<li>{}</li>".format(album.title)
                  for album in albums]
        message = """
        Nous avons trouvé les albums correspondant à votre requête ! Les voici :
        <ul>
            {}
        </ul>
    """.format("</li><li>".join(albums))

    return HttpResponse(message)
