from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Album
# Create your views here.


def index(request):
    albums = Album.objects.filter(
        available=True).order_by('created_at')[:12]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):

    albums_list = Album.objects.filter(
        available=True)
    paginator = Paginator(albums_list, 9)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If not an integer, deliver first page of results
        albums = paginator.page(1)
    except EmptyPage:
        # if page is out of range, delive last page with results
        albums = paginator.page(paginator.num_pages)
    context = {'albums': albums, 'paginate': True}
    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
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
