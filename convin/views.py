from .settings import BASE_DIR
import os
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Google standard libraries

from apiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "convin/client_secret.json")
SCOPES = ['https://www.googleapis.com/auth/calendar']

# /rest/v1/calendar/init/ -> GoogleCalendarInitView()

def GoogleCalendarInitView(request):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes = SCOPES)
            creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    return redirect('redirect')

# /rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()

def GoogleCalendarRedirectView(request):
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        events_res = service.events().list(calendarId='primary').execute()
        events = events_res.get('items', [])
        # print(events[0])
        return render(request, 'events.html', {'events': events})
    else:
        return HttpResponse("Getting events failed. Please check views. Try again")
