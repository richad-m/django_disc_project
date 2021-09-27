from django.shortcuts import render

from .models import Album
# Create your views here.


def index(request):
    albums = Album.objects.filter(
        available=True).order_by('created_at')[:12]
    # albums = ["{}".format(album) for album in all_albums]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):
    albums = Album.objects.filter(
        available=True)
    context = {'albums': albums}
    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    # artists = " ".join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    return render(request, 'store/detail.html', context)


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
        title = "Aïe, nous n'avons trouvé aucun résultat"
    else:
        title = "Résultat(s) pour la requête '%s'" % query
    context = {
        'albums': albums,
        'title': title
    }

    return render(request, 'store/search.html', context)
