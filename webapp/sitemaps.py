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
