from __future__ import print_function
from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import routers, serializers, viewsets, response
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from django.http import HttpResponse, JsonResponse
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pycronofy
from opentok import OpenTok
import random
from django.http import HttpResponse
from django.template import loader
from fbchat import Client
from fbchat.models import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@api_view(['GET'])
@permission_classes([AllowAny])
def get_personal_tasks(request):
    projs = Project.objects.filter(name = 'personal')
    proj = projs[0]
    tasks = Task.objects.filter(project = proj)
    output = []
    for i in tasks:
        output.append(i.values())
    
    return Response(output)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_personal_tasks(request):
    data = request.data
    projs = Project.objects.filter(name = 'personal')
    proj = projs[0]
    task = Task(name = data['name'], type=data['type'], due = data['due'], status= data['status'], project= proj)
    task.save()
    return Response(task.values())

@api_view(['POST'])
@permission_classes([AllowAny])
def update_personal_tasks(request):
    data = request.data
    projs = Project.objects.filter(name = 'personal')
    proj = projs[0]
    task = Task.objects.filter(project = proj, name=data['name'])[0]  
    task.name = data['name']
    task.type=data['type']
    task.due = data['due']
    task.status= data['status']
    task.project= proj
    task.save()
    return Response(task.values())

@api_view(['POST'])
@permission_classes([AllowAny])
def archive_personal_tasks(request):
    data = request.data
    task = Task.objects.filter(name = data['name'])[0]
    task.archived = True
    task.save()
    return Response(True)

@api_view(['POST'])
@permission_classes([AllowAny])
def delete_personal_tasks(request):
    data = request.data
    task = Task.objects.filter(name = data['name'])[0]
    task.delete()
    return Response(True)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_tasks(request):
    projs = Project.objects.filter(name = 'work')
    proj = projs[0]
    tasks = Task.objects.filter(project = proj)
    output = []
    for i in tasks:
        output.append(i.values())
    
    return Response(output)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_work_tasks(request):
    data = request.data
    projs = Project.objects.filter(name = 'work')
    proj = projs[0]
    task = Task(name = data['name'], type=data['type'], due = data['due'], status= data['status'], project= proj)
    task.save()
    print('xxx')
    client = Client("goldman8hacks@gmail.com", "password142")
    print('yyyy')
    msg = "You have a work task due on " + data['due']
    userid = "100003569142613"
    w = client.send(Message(text=msg), thread_id=userid, thread_type=ThreadType.USER)

    return Response(w)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_work_tasks(request):
    data = request.data
    projs = Project.objects.filter(name = 'work')
    proj = projs[0]
    task = Task.objects.filter(project = proj, name=data['name'])[0]  
    task.name = data['name']
    task.type=data['type']
    task.due = data['due']
    task.status= data['status']
    task.project= proj
    task.save()
    return Response(task.values())

@api_view(['POST'])
@permission_classes([AllowAny])
def archive_work_tasks(request):
    data = request.data
    task = Task.objects.filter(name = data['name'])[0]
    task.archived = True
    task.save()
    return Response(True)

@api_view(['POST'])
@permission_classes([AllowAny])
def delete_work_tasks(request):
    data = request.data
    task = Task.objects.filter(name = data['name'])[0]
    task.delete()
    return Response(task)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@api_view(['GET'])
@permission_classes([AllowAny])
def get_goog(request):
    output = get_google_calendar_events()
    return Response(output)

def get_google_calendar_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    with open('manager/token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=30, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    upcoming = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        try:
            upcoming.append((event['summary'], datetime.datetime.strptime(event['start']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S'), datetime.datetime.strptime(event['end']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S'), random.choice(["blue", "red", "green"]), True))
        except KeyError:
            upcoming.append((event['summary'], datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d'), datetime.datetime.strptime(event['end']['date'], '%Y-%m-%d')-datetime.timedelta(days=1), random.choice(["blue", "red", "green"]), False))

    return(upcoming)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_out(request):
    output = get_outlook_calendar_events()
    return Response(output)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all(request):
    out = get_outlook_calendar_events()
    goog = get_google_calendar_events()
    out.extend(goog)
    return Response(out)

def get_outlook_calendar_events():

    CLIENT_ID = 'oVjF0tuVTnGiEKfaKfgtOt6dQDVjr5IZ'
    SECRET_ID = '54J2YKoVlNBX-yTk1Nwm6Yx5vLLBdglBlp-hUP7YSRFdOKk6D5vRpXhIifWzkkK_PBFUVlbYvudb4PgLq9m9GA'

    cronofy = pycronofy.Client(access_token="cF-JVep9yCEUk3jxDNDi1rFzedvxXXsj")
    events = cronofy.read_events()

    holidays = ['Christmas Day', 'Boxing Day', 'Boxing Day Bank Holiday', 'New Year\'s Day', 'New Year\'s Day (2nd Day) (Scotland)', 'New Year\'s Day (2nd Day) (Scotland) (Observed)',
                'St. Patrick\'s Day (N. Ireland)', 'Good Friday', 'Easter Day', 'Easter Monday', 'May Day Bank Holiday', 'Spring Bank Holiday', 'Battle of the Boyne (N. Ireland)',
                'August Bank Holiday (Scotland)']

    upcoming = []

    for event in events.all():
        if event['summary'] not in holidays:
            try:
                upcoming.append((event['summary'], datetime.datetime.strptime(event['start'][:19], '%Y-%m-%dT%H:%M:%S'), datetime.datetime.strptime(event['end'][:19], '%Y-%m-%dT%H:%M:%S'), random.choice(["blue", "red", "green"]), True))
            except ValueError:
                upcoming.append((event['summary'], datetime.datetime.strptime(event['start'][:19], '%Y-%m-%d'), datetime.datetime.strptime(event['end'][:19], '%Y-%m-%d')-datetime.timedelta(days=1), random.choice(["blue", "red", "green"]), False))
    return(upcoming)



@api_view(['POST'])
@permission_classes([AllowAny])
def add_meeting(request):

    api_key = "47084204"  # Replace with your OpenTok API key.
    api_secret = "3e487ed7f77e32f86f561244ee1571618a485458"  # Replace with your OpenTok API secret.

    data = request.data

    opentok = OpenTok(api_key, api_secret)
    session = opentok.create_session()
    session_id = session.session_id
    token = opentok.generate_token(session_id)

    meeting = Meeting(name=data['name'], session_id=session_id, token=token,
                      start_date=data['start_date'], end_date=data['end_date'],
                      colour=data['colour'], summary=data['summary'], fullday=data['fullday'])
    meeting.save()
    return Response(meeting.values())


def get_meeting(request):
    meetings = Meeting.objects.all()
    output = []
    for m in meetings:
        output.append(m.values())

    session = meetings[0].session_id
    token = meetings[0].token
    data = {'session':session, 'token':token}

    #template = loader.get_template('manager/templates/index.html')

    return render( request,'index.html', data )


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_meeting(request):
    data = request.data
    meeting = Meeting.objects.filter(name = data['name'][0])
    meeting.delete()
    return Response(meeting)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_reminder(request):

    data = request.data

    reminder = Reminder(name=data['name'], date=data['date'], message=data['message'], uid=data['uid'])

    reminder.save()
    return Response(reminder.values())


@api_view(['GET'])
@permission_classes([AllowAny])
def get_reminder(request):
    reminders = Reminder.objects.all()
    output = []
    for r in reminders:
        output.append(r.values())

    return Response(output)