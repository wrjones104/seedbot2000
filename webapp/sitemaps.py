from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# This class handles static pages like your homepage, about page, etc.
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        # Return a list of the URL names for your static pages
        return ['home', 'quick-roll', 'preset-list', 'my-profile', 'tune-up']
    
    def location(self, item):
        return reverse(item)

# Example for dynamic pages
# class PresetSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#
#     def items(self):
#         # Return a queryset of public presets
#         return Preset.objects.filter(public=True)
#
#     def lastmod(self, obj):
#         # Return the last modified date for each preset
#         return obj.updated_at