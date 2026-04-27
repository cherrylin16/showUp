from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ShowUpRSVPs
from django.db import connection

def index(request):
    invites = None
    userID = request.user.userID
    # invites = ShowUpRSVPs.objects.filter(user=userID)
    with connection.cursor() as cursor:
        cursor.execute('SELECT e.eventName, e.date, e.time, e.theme, u.firstName, u.lastName, r.status, r.RSVPID FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s;', [userID, userID])
        rows = cursor.fetchall()

    search = request.GET.get('search', '')
    filtered = request.GET.get('filter', 'All')
    with connection.cursor() as cursor:
        if search:
            cursor.execute('SELECT e.eventName, e.date, e.time, e.theme, u.firstName, u.lastName, r.status, r.RSVPID FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND e.eventName LIKE %s;', [userID, userID, ('%' + search + '%')])
            rows = cursor.fetchall()
        
        if filtered == 'No_RSVP':
            cursor.execute('SELECT e.eventName, e.date, e.time, e.theme, u.firstName, u.lastName, r.status, r.RSVPID FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND r.status IS NULL;', [userID, userID])
            rows = cursor.fetchall()
        elif filtered != "All":
            cursor.execute('SELECT e.eventName, e.date, e.time, e.theme, u.firstName, u.lastName, r.status, r.RSVPID FROM ShowUp_Users u JOIN ShowUp_RSVPs r JOIN ShowUp_Events e ON u.userID = r.userID AND r.eventID = e.eventID WHERE u.userID = %s AND e.hostID <> %s AND r.status = %s;', [userID, userID, filtered])
            rows = cursor.fetchall()
    
    invites = [{"eventName": r[0], "date": r[1], "time": r[2], "theme": r[3], "firstName": r[4], "lastName": r[5], "status": r[6], "rsvpID": r[7]} for r in rows]
    context = {"user_invites" : invites, "search": search}
    return render(request, "invites/index.html", context)

def rsvp_form(request):
    userID = request.user.userID

    if request.method == "POST":
        eventID = request.POST.get('eventID')
        rsvpID = request.POST.get('rsvpID')
        status = request.POST.get('rsvp')
        comment = request.POST.get('comment')

        # User clicked RSVP from dashboard
        if eventID:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT RSVPID, status, message
                    FROM ShowUp_RSVPs
                    WHERE eventID = %s AND userID = %s;
                    ''',
                    [eventID, userID]
                )
                rows = cursor.fetchone()

            if not rows:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT hostID FROM ShowUp_Events WHERE eventID = %s;',
                        [eventID]
                    )
                    host_row = cursor.fetchone()

                if host_row and host_row[0] == userID:
                    return redirect("dashboard_home")

                return HttpResponse("You are not invited to this event.", status=403)

            rsvpID = rows[0]
            status = rows[1]
            comment = rows[2]

            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT itemName, quantity
                    FROM ShowUp_Items
                    WHERE eventID = %s AND userID = %s;
                    ''',
                    [eventID, userID]
                )
                existing_items = {
                    row[0]: row[1]
                    for row in cursor.fetchall()
                }

        # User submitted RSVP form
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT eventID
                    FROM ShowUp_RSVPs
                    WHERE RSVPID = %s AND userID = %s;
                    ''',
                    [rsvpID, userID]
                )
                event_row = cursor.fetchone()

            if not event_row:
                return HttpResponse("RSVP not found.", status=404)

            eventID = event_row[0]

            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT itemName, quantity
                    FROM ShowUp_Items
                    WHERE eventID = %s AND userID = %s;
                    ''',
                    [eventID, userID]
                )
                existing_items = {
                    row[0]: row[1]
                    for row in cursor.fetchall()
                }

            if status:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        UPDATE ShowUp_RSVPs
                        SET status = %s, message = %s
                        WHERE RSVPID = %s AND userID = %s;
                        ''',
                        [status, comment, rsvpID, userID]
                    )

                    item_names = request.POST.getlist("item_name[]")
                    quantities = request.POST.getlist("quantity[]")

                    submitted_items = {}

                    for name, qty in zip(item_names, quantities):
                        name = name.strip()

                        if name and qty:
                            submitted_items[name] = int(qty)

                    # Insert or update submitted items
                    for name, qty in submitted_items.items():
                        if name in existing_items:
                            if existing_items[name] != qty:
                                cursor.execute(
                                    '''
                                    UPDATE ShowUp_Items
                                    SET quantity = %s
                                    WHERE eventID = %s AND userID = %s AND itemName = %s;
                                    ''',
                                    [qty, eventID, userID, name]
                                )
                        else:
                            cursor.execute(
                                '''
                                INSERT INTO ShowUp_Items (eventID, itemName, quantity, userID)
                                VALUES (%s, %s, %s, %s);
                                ''',
                                [eventID, name, qty, userID]
                            )

                    # Delete removed items
                    for name in existing_items:
                        if name not in submitted_items:
                            cursor.execute(
                                '''
                                DELETE FROM ShowUp_Items
                                WHERE eventID = %s AND userID = %s AND itemName = %s;
                                ''',
                                [eventID, userID, name]
                            )

                return redirect("invites:index")

        # Load RSVP details page
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT e.eventName, e.date, e.time, e.theme, e.description,
                       e.location, host.firstName, host.lastName,
                       r.status, r.message, r.RSVPID
                FROM ShowUp_RSVPs r
                JOIN ShowUp_Events e ON r.eventID = e.eventID
                JOIN ShowUp_Users host ON e.hostID = host.userID
                WHERE r.RSVPID = %s AND r.userID = %s;
                ''',
                [rsvpID, userID]
            )
            rows = cursor.fetchone()

            if not rows:
                return HttpResponse("RSVP not found.", status=404)

            invite = {
                "eventName": rows[0],
                "date": rows[1],
                "time": rows[2],
                "theme": rows[3],
                "description": rows[4],
                "location": rows[5],
                "firstName": rows[6],
                "lastName": rows[7],
                "status": rows[8],
                "message": rows[9],
                "rsvpID": rows[10],
            }

            cursor.execute(
                '''
                SELECT itemName, quantity
                FROM ShowUp_Items
                WHERE eventID = %s AND userID = %s;
                ''',
                [eventID, userID]
            )
            item_rows = cursor.fetchall()

            items = [
                {
                    "itemName": row[0],
                    "quantity": row[1],
                }
                for row in item_rows
            ]

        context = {
            "user_invite": [invite],
            "items": items,
            "rsvpID": rsvpID,
            "status": status,
            "comment": comment,
            "user": userID,
        }

        return render(request, "invites/rsvp_form.html", context)

    return render(request, "invites/index.html")