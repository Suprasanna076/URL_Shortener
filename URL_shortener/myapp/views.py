from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LongToShort
from django.utils import timezone # Import timezone

# For parsing user agent (basic approach)
import re

# Create your views here.
def hello_world(request):
    return HttpResponse("HelloWorld!")

def home_page(request):
    context = {
        "submitted": False,
        "error": False
    }

    if request.method == 'POST':
        data = request.POST
        long_url = data['longurl']
        custom_name = data['custom_name']

        # CREATE
        try:
            obj = LongToShort(long_url=long_url, short_url=custom_name)
            obj.save()

            # READ
            date = obj.date
            clicks = obj.clicks

            context["long_url"] = long_url
            # CORRECTED LINE: Pass only the short_url (the alias) to the template for analytics link
            context["short_url"] = custom_name # <--- CHANGE THIS LINE
            # The full URL for display/copy can be built in the template or passed separately if needed
            context["full_short_url_display"] = request.build_absolute_uri() + custom_name # New context variable for display

            context["date"] = date
            context["clicks"] = clicks
            context["submitted"] = True

        except Exception as e:
            context["error"] = True
            if "UNIQUE constraint failed" in str(e):
                context["error_message"] = "The custom URL name you chose already exists. Please pick another one."
            else:
                context["error_message"] = "Something went wrong. Please check your URL and try again."
            print(f"Error in home_page (POST): {e}")

    else:
        print("User not sending anything (GET request)")

    return render(request, "index.html", context)

# ... (rest of your views.py remains the same) ...

def redirect_url(request, short_url):
    try:
        obj = get_object_or_404(LongToShort, short_url=short_url) # Use get_object_or_404 for cleaner 404

        obj.clicks += 1
        obj.last_accessed = timezone.now() # Update last accessed time

        # Capture additional analytics data
        obj.user_agent = request.META.get('HTTP_USER_AGENT', '')
        obj.referrer = request.META.get('HTTP_REFERER', '')
        obj.ip_address = get_client_ip(request) # Helper function to get IP

        obj.save()
        return redirect(obj.long_url)
    except LongToShort.DoesNotExist: # get_object_or_404 handles this, but keeping for clarity if not used
        return HttpResponse("No such short URL exist", status=404) # Return 404 status
    except Exception as e:
        print(f"Error redirecting URL '{short_url}': {e}") # Log the error
        return HttpResponse("An error occurred during redirection.", status=500)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def all_analytics(request):
    # CORRECTED: Order by 'date' as 'created_at' does not exist in your model
    rows = LongToShort.objects.all().order_by('-date')
    context = {
        "rows": rows # Pass the queryset directly
    }
    return render(request, "all-analytics.html", context)

# Modified analytics view to correctly pass data for a single short_url
def analytics(request, short_url):
    try:
        link_obj = get_object_or_404(LongToShort, short_url=short_url)

        context = {
            # It's better to stick to one name. Let's use 'obj' directly for consistency with your template
            "obj": link_obj, # This is the main LongToShort object for this URL

            # Your template also expects 'cols' for the first section
            "cols": [link_obj], # Wrap it in a list as analytics.html uses {% for obj in cols %}

            "long_url": link_obj.long_url,
            "short_url": link_obj.short_url,
            "date": link_obj.date,
            "clicks": link_obj.clicks,
            # 'created_at' does not exist in your LongToShort model, it's 'date'
            # Remove or correct 'created_at': link_obj.created_at,
            "last_accessed": link_obj.last_accessed,
            "user_agent": link_obj.user_agent,
            "referrer": link_obj.referrer,
            "ip_address": link_obj.ip_address,

            # Placeholder chart data (these are still hardcoded examples)
            "countries": ["USA", "India", "Germany"],
            "number_of_clicks": [50, 30, 20], # This should match 'clicks' for the bar chart
            "desktop": 70,
            "mobile": 30,
        }
        return render(request, "analytics.html", context)
    except LongToShort.DoesNotExist:
        return HttpResponse("No analytics available for this short URL.", status=404)
    except Exception as e:
        print(f"Error fetching analytics for '{short_url}': {e}")
        return HttpResponse("An error occurred while fetching analytics.", status=500)