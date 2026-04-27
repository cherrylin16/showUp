from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date, time
from django.db import connection

# import forms
from .forms import EventPostForm
from .models import EventPost, Budget, EventPhoto, Orders, Catering, Caterer
from invites.models import ShowUpRSVPs

# querying
from django.db.models import Q
import base64


# Create your views here.
@login_required
def dashboard_home(request):
    form = EventPostForm()
    posts = EventPost.objects.filter(
        Q(author=request.user) |
        Q(id__in=ShowUpRSVPs.objects.filter(user=request.user).values_list("event_id", flat=True))
    ).distinct()

    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    time_filter = request.GET.get('time', '')

    if query:
        posts = posts.filter(
            Q(author__firstName__icontains=query) |
            Q(author__lastName__icontains=query) |
            Q(event_name__icontains=query) |
            Q(event_description__icontains=query)
        ).distinct()

    view_filter = request.GET.get('view', 'all')

    if view_filter == 'hosting':
        posts = posts.filter(author=request.user)
 

    if date_filter:
        posts = posts.filter(date=date_filter)

    if time_filter:
        posts = posts.filter(time=time_filter)
    

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
        try:
            for photo in post.photos.all():
                encoded = base64.b64encode(bytes(photo.image)).decode("utf-8")  # bytes() fixes memoryview
                post.display_photos.append({
                    "id": photo.id,
                    "image": encoded,
                })
        except Exception as e:
            print(f"Photo error for post {post.id}: {e}")

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
        if request.POST.get('delete_post_id'):
            post_id = request.POST.get('delete_post_id')
            EventPost.objects.filter(id=post_id, author=request.user).delete()
            return redirect('dashboard_home')

        form = EventPostForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save the Event
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            catering_budget = form.cleaned_data.get("catering_budget") or 0
            supplies_budget = form.cleaned_data.get("supplies_budget") or 0
            total_budget = catering_budget + supplies_budget

            Budget.objects.create(
                event=post,
                catering=catering_budget,
                party_supplies=supplies_budget,
                total_budget=total_budget      
            )

            caterer_name = form.cleaned_data.get("caterer_name")
            caterer_phone = form.cleaned_data.get("caterer_phone")
            caterer_location = form.cleaned_data.get("caterer_address")

            caterer = None
            if caterer_name and caterer_name.strip(): 
                caterer, created = Caterer.objects.get_or_create(
                    name=caterer_name.strip(),
                    defaults={
                        "phone": caterer_phone or "",
                        "caterer_location": caterer_location or ""
                    }
                )
                if not created:
                    caterer.phone = caterer_phone or caterer.phone
                    caterer.save()

            if caterer:
                catering_record = Catering.objects.create(
                    event=post,
                    caterer=caterer, 
                    special_instructions=""
                )

                # 5. Handle Orders (Dish list)
                dish_names = request.POST.getlist("dish_name[]")
                quantities = request.POST.getlist("quantity[]")
                prices = request.POST.getlist("price[]")

                for name, qty, price in zip(dish_names, quantities, prices):
                    if name.strip():
                        Orders.objects.create(
                        cateringID=catering_record,
                        dishName=name.strip(),
                        quantity=int(qty) if qty else 0,
                        price=float(price) if price else 0.0
                        )

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