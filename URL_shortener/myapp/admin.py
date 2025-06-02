from django.contrib import admin
from .models import LongToShort

class LongToShortAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'long_url', 'clicks', 'created_at', 'last_accessed', 'user_agent', 'ip_address', 'referrer')
    search_fields = ('short_url', 'long_url', 'ip_address')
    list_filter = ('created_at', 'last_accessed') # Allows filtering by date
    search_fields = ('short_url', 'long_url')
    ordering = ('-date',) 
admin.site.register(LongToShort, LongToShortAdmin)
