from django.db import models
from django.urls import reverse

class Event(models.Model): 
    dmeva_code  = models.CharField(max_length=20) 
    dmeva_fecha = models.DateField()
    location    = models.OneToOneField('Location', on_delete=models.SET_NULL, null=True, verbose_name='Ubicación') 
    mapa        = models.ImageField(upload_to='mapa/', blank=True, verbose_name='Mapa de Ubicación')     ### models.PolygonField(upload_to='mapa/')
    grafico     = models.ImageField(upload_to='grafico/', blank=True, verbose_name='Superficie Grafico')
    def __str__(self): 
        return self.dmeva_code  

class Informe(models.Model):
    informe_code= models.CharField(max_length=20)
    event       = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    satimage1   = models.ForeignKey('SatImage', null=True, on_delete=models.SET_NULL, related_name='informe1')
    satimage2   = models.ForeignKey('SatImage', null=True, on_delete=models.SET_NULL, related_name='informe2') 
    title       = models.CharField(max_length=200, verbose_name='Titulo')
    fecha       = models.DateField()
    def __str__(self): 
        return self.informe_code  
    def get_absolute_url(self):
        return reverse('informe_detail', args=[str(self.id)])

class SatImage(models.Model): 
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Evento')
    fuente      = models.CharField(max_length=50)
    banda       = models.CharField(max_length=50)
    fecha       = models.DateField()
    image       = models.ImageField(upload_to='satimages', verbose_name='Imagen')  
    def __str__(self): 
        return str(self.event) + " " + str(self.fuente) + " " + str(self.banda)    

class Area(models.Model):   
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Evento')
    location    = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Ubicación')  
    superficie  = models.DecimalField(max_digits=8, decimal_places=2)
    hectarea    = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Hectáreas')
    percentage  = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Porcentaje')

    def calculate(self):         ##  also need to change  ajax_calculate() function 
        try:
          calc_value = float(self.hectarea) / float(self.superficie) * 100
        except:
            print("An exception occurred")
        return calc_value

    def save(self, *args, **kwargs):
        self.percentage =  self.calculate() 
        super(Area, self).save(*args, **kwargs)

    def __str__(self): 
        return str(self.event) + " " + str(self.location) 

class Location(models.Model):  
    location_code  = models.CharField(max_length=6, primary_key=True, verbose_name='Código') 
    province    = models.CharField(max_length=50, null=True, verbose_name='Provincia')
    canton      = models.CharField(max_length=50, null=True, verbose_name='Cantón')
    parroquia   = models.CharField(max_length=50, null=True, verbose_name='Parroquia')
    def __str__(self): 
        return self.location_code + " " + self.province + " " + self.canton + " " + self.parroquia

# class Provincia(models.Model): 
#     name        = models.CharField(max_length=30)

# class Canton(models.Model): 
#     name        = models.CharField(max_length=30)
#     provincia   = models.ForeignKey(Provincia, on_delete=models.SET_NULL) 

# class Parroquia(models.Model): 
#     name        = models.CharField(max_length=30)
#     canton      = models.ForeignKey(Canton, on_delete=models.SET_NULL) 

