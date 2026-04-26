from django.shortcuts import render
from django.http import HttpResponse
from .models import ShowUpRSVPs
from django.db import connection

def index(request):
    invites = None
    userID = request.user.userID
    invites = ShowUpRSVPs.objects.filter(user=userID)
   
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT e.eventName, u.firstName, u.lastName, r.status FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s;', [userID, userID])
    #     invites = cursor.fetchall()
        
    # search = request.GET.get('search', '')
    # filtered = request.GET.get('filter', 'all')
    # with connection.cursor() as cursor:
    #     if search:
    #         cursor.execute('SELECT e.eventName, u.firstName, u.lastName, r.status FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND e.eventName ILIKE %s;', [userID, userID, search])
        
    #     if filtered == 'No_RSVP':
    #         cursor.execute('SELECT e.eventName, u.firstName, u.lastName, r.status FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND r.status IS NULL;', [userID, userID])
    #     elif filtered != "All":
    #         cursor.execute('SELECT e.eventName, u.firstName, u.lastName, r.status FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND r.status = %s;', [userID, userID, filtered])
    #     invites = cursor.fetchall()
    
    context = {"user_invites" : invites}
    return render(request, "invites/index.html", context)

def rsvp_form(request):
    return render(request, "invites/rsvp_form.html")
