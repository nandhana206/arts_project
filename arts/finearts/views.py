from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Event
from django.contrib.auth import authenticate, login,logout

# Register View
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        admission_number = request.POST.get('admission_number')
        department = request.POST.get('department')

        # Check if admission number is unique
        if Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, 'Admission number already exists.')
            return render(request, 'register.html')

        # Create a new student
        Student.objects.create(name=name, admission_number=admission_number, department=department)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password match an existing admission number
        if Student.objects.filter(admission_number=username).exists() and username == password:
            request.session['user'] = username
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


# Dashboard View
def dashboard_view(request):
    """
    Dashboard view that handles user profile and event registration.
    """
    # Check if user is logged in
    user = request.session.get('user', None)
    if not user:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    # Fetch the student's details
    try:
        student = Student.objects.get(admission_number=user)
    except Student.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('login')

    # Event registration logic
    if request.method == 'POST':
        # Retrieve selected offstage, onstage, and group events from the form
        selected_offstage_events = request.POST.getlist('offstage_events[]')
        selected_onstage_events = request.POST.getlist('onstage_events[]')
        selected_group_events = request.POST.getlist('group_events[]')

        # Combine group events with onstage events
        selected_onstage_events.extend(selected_group_events)  # Add group events to onstage events

        # Limit registration to a maximum of 3 offstage events and 3 onstage events (including group events)
        if len(selected_offstage_events) > 3:
            messages.error(request, 'You can only register for a maximum of 3 offstage events.')
        elif len(selected_onstage_events) > 3:
            messages.error(request, 'You can only register for a maximum of 3 onstage events.')
        elif len(selected_offstage_events) + len(selected_onstage_events) > 6:
            messages.error(request, 'You can only register for a total of 6 events (3 offstage and 3 onstage).')
        else:
            # Clear existing events before adding new ones
            student.events.clear()

            # Register the selected offstage events
            for event_name in selected_offstage_events:
                event, _ = Event.objects.get_or_create(name=event_name, category='offstage')
                student.events.add(event)

            # Register the selected onstage events (including group events)
            for event_name in selected_onstage_events:
                event, _ = Event.objects.get_or_create(name=event_name, category='onstage')
                student.events.add(event)

            messages.success(request, 'You have successfully registered for the selected events.')
            return redirect('user_profile')  # Redirect to the user profile page

    # Fetch all available events (onstage and offstage)
    offstage_events = Event.objects.filter(category='offstage')
    onstage_events = Event.objects.filter(category='onstage')

    # Fetch registered events
    registered_events = student.events.all()

    # Render the dashboard template with necessary context
    return render(request, 'dashboard.html', {
        'student': student,
        'registered_events': registered_events,
        'offstage_events': offstage_events,
        'onstage_events': onstage_events,
    })


# User Profile View
def user_profile_view(request):
    """
    View to display the user's profile, including name, department, and selected events.
    """
    user = request.session.get('user', None)
    if not user:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    try:
        student = Student.objects.get(admission_number=user)
    except Student.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('login')

    # Fetch registered events
    registered_events = student.events.all()

    return render(request, 'user_profile.html', {
        'student': student,
        'registered_events': registered_events,
    })

def logout_view(request):
    logout(request)
    return redirect('login')
