from django.db import models

class LongToShort(models.Model):
    long_url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    # New fields for enhanced analytics
    created_at = models.DateTimeField(auto_now_add=True) # More precise timestamp
    last_accessed = models.DateTimeField(auto_now=True) # To track last click time
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.short_url} -> {self.long_url}"