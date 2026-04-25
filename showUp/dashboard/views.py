from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# import forms
from .forms import EventPostForm
from .models import EventPost


# Create your views here.
def dashboard_home(request):
    # return HttpResponse("Setting up our initial Django app.")

    # Create an empty instance of the form
    form = EventPostForm() 
    
    context = {
        'form': form,
    }

    return render(request, "dashboard/home.html", context)


def create_event_post(request):
    if request.method == 'POST':
        # Handle deletion
        # if 'delete_post_id' in request.POST:
        #     post_id = request.POST.get('delete_post_id')
        #     CarpoolPost.objects.filter(id=post_id, author=request.user).delete()
        #     messages.success(request, 'Post deleted successfully.')
        #     return redirect('driver dashboard')

        # Handle creation
        form = EventPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.save()
            messages.success(request, 'Event post created successfully!')
            return redirect('dashboard_home')
        
    return redirect('dashboard_home')



