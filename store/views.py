from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Album, Contact, Booking
from .forms import ContactForm
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
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                # If a contact is not registered, create a new one.
                contact = Contact.objects.create(
                    email=email,
                    name=name
                )
            else:
                contact = contact.first()

            album = get_object_or_404(Album, id=album_id)
            booking = Booking.objects.create(
                contact=contact,
                album=album
            )
            album.available = False
            album.save()
            context = {
                'album_title': album.title
            }
            return render(request, 'store/thanks.html', context)
        else:
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
    else:
        form = ContactForm()
    context['form'] = form
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
