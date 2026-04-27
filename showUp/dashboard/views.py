from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date, time
from django.db import connection

# import forms
from .forms import EventPostForm
from .models import EventPost

# querying
from django.db.models import Q


# Create your views here.
@login_required
def dashboard_home(request):
    form = EventPostForm()
    posts = EventPost.objects.all()

    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    time_filter = request.GET.get('time', '')

    if query:
        posts = posts.filter(
            Q(host_name__icontains=query) |
            Q(event_name__icontains=query) |
            Q(location__icontains=query) |
            Q(event_description__icontains=query)
        ).distinct()

    view_filter = request.GET.get('view', 'all')

    if view_filter == 'hosting':
        posts = posts.filter(author=request.user)
    elif view_filter == 'attending':
        posts = posts.filter(attendees=request.user)

    if date_filter:
        posts = posts.filter(date=date_filter)

    if time_filter:
        posts = posts.filter(pickup_time__icontains=time_filter)
    

    # Separate active and previous posts
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()

    active_posts = []
    previous_posts = []

    for post in posts:
        post_date = getattr(post, "date", None)
        post_time = getattr(post, "time", None)

        if post_date is None or post_time is None:
            active_posts.append(post)
            continue

        if hasattr(post_date, "date"):
            post_date = post_date.date()

        post_datetime = datetime.combine(post_date, post_time)
        current_datetime = datetime.now()

        if post_datetime > current_datetime:
            active_posts.append(post)
        else:
            previous_posts.append(post)

    for post in active_posts + previous_posts:
        post.display_photos = []

        for photo in post.photos.all():
            encoded = base64.b64encode(photo.image).decode("utf-8")
            post.display_photos.append({
                "id": photo.id,
                "image": encoded,
            })

        post.invite_list = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT u.firstName, u.lastName, r.status, r.RSVPID FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE e.eventID = %s;', [post.id])
            rows = cursor.fetchall()
            post.invite_list = [{"firstName": r[0], "lastName": r[1], "status": r[2]} for r in rows]
            
    return render(request, "dashboard/home.html", {
        'active_posts': active_posts,
        'previous_posts': previous_posts,
        'query': query,
        'form': form,
        'view_filter': view_filter
    })
    
    
    
@login_required
def create_event_post(request):
    if request.method == 'POST':
        #Handle deletion
        if request.POST.get('delete_post_id'):
            post_id = request.POST.get('delete_post_id')
            EventPost.objects.filter(id=post_id, author=request.user).delete()
            return redirect('dashboard_home')

        # Handle creation
        form = EventPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard_home')
        
    return redirect('dashboard_home')




from .models import EventPost, EventPhoto
from .forms import EventPhotoForm
import base64

@login_required
def upload_event_photo(request, post_id):
    post = get_object_or_404(EventPost, id=post_id)

    if request.method == "POST":
        form = EventPhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.event = post
            photo.save()

        else:
            print(form.errors)

    return redirect("dashboard_home")


@login_required
def delete_event_photo(request, photo_id):
    photo = get_object_or_404(EventPhoto, id=photo_id)

    if photo.event.author == request.user:
        photo.delete()

    return redirect("dashboard_home")

@login_required
def invite_guest(request, post_id):
    post = get_object_or_404(EventPost, id=post_id)

    if request.method == "POST":
        guest = request.POST.get('invited')
        with connection.cursor() as cursor:
            cursor.execute('SELECT userID FROM ShowUp_Users WHERE email = %s;', [guest])
            rows = cursor.fetchone()
            if rows:
                cursor.execute('INSERT INTO ShowUp_RSVPs (eventID, userID) VALUES (%s, %s);', [post.id, rows[0]])

    return redirect("dashboard_home")