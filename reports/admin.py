from django.contrib import admin
from .models import Event, Informe, SatImage, Area, Location

# Register your models here.

# admin.site.register(Informe)  ## Informe should be created using the custom app

admin.site.register(Location)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    raw_id_fields = ["location"]

class AreaAdmin(admin.ModelAdmin):
    readonly_fields=('percentage', )
    raw_id_fields = ["location"]
    list_display = ['event', 'location']
    ordering = ['event', 'location'] 
admin.site.register(Area, AreaAdmin)

class InformeAdmin(admin.ModelAdmin):
    list_display = ['informe_code', 'title', 'fecha', 'event', 'satimage1', 'satimage2' ]
admin.site.register(Informe, InformeAdmin)

class SatImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'fuente', 'banda', 'fecha', 'image']
admin.site.register(SatImage, SatImageAdmin)
