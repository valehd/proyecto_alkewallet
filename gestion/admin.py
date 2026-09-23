from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion, Etiqueta


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email", "telefono")
    search_fields = ("nombre", "email")


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("numero_cuenta", "cliente", "saldo")
    search_fields = ("numero_cuenta", "cliente__nombre")


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("id", "cuenta", "tipo", "monto", "fecha", "descripcion")
    search_fields = ("tipo", "descripcion", "cuenta__numero_cuenta")
    list_filter = ("tipo", "fecha")
    ordering = ("-fecha",)