from django.db import models
from django.contrib.auth.models import AbstractUser

class Direcciones(models.Model):
    nombre = models.CharField(max_length = 100)
    codename = models.CharField(max_length = 5)
    see_in_select = models.BooleanField(default = True)
    see_in_list = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    titular = models.OneToOneField('direccion.Usuarios', on_delete = models.CASCADE, null = True, blank = True)
    subdireccion = models.ForeignKey('self', on_delete = models.SET_NULL, null = True, blank = True, related_name = 'subdir')
    def __str__(self):
        return '{}'.format(self.nombre)

class Usuarios(AbstractUser):
    direccion = models.ForeignKey(Direcciones, null = True, blank = True, on_delete = models.PROTECT)
    avatar = models.ImageField(upload_to = 'avatar/', null = True, blank = True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Permisos(models.Model):
    assign_all = models.BooleanField(default = False)
    see_all = models.BooleanField(default = False)
    see_panel = models.BooleanField(default = False)
    delete_all = models.BooleanField(default = False)
    change_priority = models.BooleanField(default = False)
    usuario = models.OneToOneField(Usuarios, blank = True, null = True, on_delete = models.CASCADE, related_name = 'permisos')

class Actividades(models.Model):
    class Meta:
        ordering = ['prioridad', '-timestamp']

    prioridad_choices = [
        (1, 'Alta'),
        (2, 'Media'),
        (3, 'Baja')
    ]
    nombre = models.CharField(max_length = 500)
    folio = models.CharField(max_length = 10, null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    comentarios = models.CharField(max_length = 700, null = True, blank = True,  default = '')
    prioridad = models.SmallIntegerField(default = 2, choices = prioridad_choices)
    direccion = models.ForeignKey(Direcciones, null = True, blank = True, related_name = 'actividades' , on_delete = models.CASCADE)
    is_cancelled = models.BooleanField(default = False)    
    usuario = models.ForeignKey(Usuarios, blank = True, on_delete = models.CASCADE)

    def get_priority_class(self):
        if self.prioridad == 1:
            return 'high'
        elif self.prioridad == 2:
            return 'medium'
        elif self.prioridad == 3:
            return 'low'
        else:
            return 'none'

    def get_priority(self):
        return dict(self.prioridad_choices).get(self.prioridad, 'No especificado')

    def get_porcent(self):
        total = self.objetivos.count()
        total_done = self.objetivos.filter(is_done = True).count()
        return getPercentActivity(total_done, total)
    
    def get_light(self):
        total = self.objetivos.count()
        total_done = self.objetivos.filter(is_done = True).count()
        return getLightActivity(total_done, total)

def act_directory_path(instance, filename):
    return 'evidencias/{0}/{1}'.format(instance.actividad.folio,filename)

class Evidencias(models.Model):
    evidencia = models.FileField(upload_to = act_directory_path, null = True, blank = True)
    nombre = models.CharField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add = True)
    actividad = models.ForeignKey(Actividades, null = True, blank = True, related_name = 'evidencias' , on_delete = models.CASCADE)

class Objetivos(models.Model):
    class Meta:
        ordering = ['end_date']

    timestamp = models.DateTimeField(auto_now_add = True, null=True)
    nombre = models.CharField(max_length = 500)
    is_done = models.BooleanField(default = False)
    actividad = models.ForeignKey(Actividades, null = True, blank = True, related_name = 'objetivos' , on_delete = models.CASCADE)
    end_date = models.DateField(null=True, editable=False)

def getPercentActivity(num, total):
    try:
        percent = (100 * num)/total
        return round(percent)
    except:
        return 0

def getLightActivity(num, total):
    red_color = '#f44336'
    green_color = '#4caf50'
    yellow_color = '#ffeb3b'
    green_light = 100
    yellow_light = 70
    try:
        percent = getPercentActivity(num, total)
        if percent == green_light:
            return green_color
        elif percent < green_light and percent >= yellow_light:
            return yellow_color
        elif percent < yellow_light:
            return red_color
    except:
        return red_color

class Correos_Notificacion(models.Model):
    correo_inst = models.EmailField(null = True, blank = True)
    correo_per = models.EmailField(null = True, blank = True)
    usuario = models.OneToOneField(Usuarios, related_name = 'correos', null = True, blank = True, on_delete = models.CASCADE)