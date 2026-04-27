from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date, time

# import forms
from .forms import EventPostForm
from .models import EventPost

# querying
from django.db.models import Q


# Create your views here.
@login_required
def dashboard_home(request):
    # return HttpResponse("Setting up our initial Django app.")

    # Create an empty instance of the form
    form = EventPostForm() 
    posts = EventPost.objects.all() # get all event posts
    
    context = {
        'form': form,
    }

    # search queries and filters
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    start_time_filter = request.GET.get('start_time', '')
    end_time_filter = request.GET.get('end_time', '')

    if query:
        posts = posts.filter(
            Q(host_name__icontains=query) |
            Q(event_name__icontains=query) |
            Q(location__icontains=query) |
            Q(caterer_address__icontains=query) |
            Q(caterer_phone__icontains=query) |
            Q(caterer_name__icontains=query) |
            Q(catering_budget__icontains=query) |
            Q(supplies_budget__icontains=query) |
            Q(date__icontains=query) |
            Q(start_time__icontains=query) |
            Q(end_time__icontains=query) |
            Q(event_description__icontains=query) 
        ).distinct()
    
    view_filter = request.GET.get('view', 'all')

    if view_filter == 'hosting':
        posts = posts.filter(author=request.user)

    elif view_filter == 'attending':
        posts = posts.filter(attendees=request.user)

    if query:
        posts = posts.filter(event_name__icontains=query)

    if date_filter:
            posts = posts.filter(date=date_filter)

    # Separate active and previous posts
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    active_posts = []
    previous_posts = []

    for post in posts:
        try:
            # Parse date and time from post
            post_date = datetime.strptime(post.date, '%Y-%m-%d').date()
            post_time = post.start_time
            
            # Check if post is in the future
            if post_date > current_date or (post_date == current_date and post_time > current_time):
                active_posts.append(post)
            else:
                previous_posts.append(post)
        except (ValueError, TypeError):
            # If date/time parsing fails, treat as active
            active_posts.append(post)

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



