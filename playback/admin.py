from django.contrib import admin
import playback.models as m

class GenreAdmin(admin.ModelAdmin):
    fields = ['name']
    class Meta:
        ordering = ['name']

admin.site.register(m.User)
admin.site.register(m.Genre)
admin.site.register(m.Artist)
admin.site.register(m.Track)