from django.urls import path

from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
    TransaccionListView,
    TransaccionCreateView,

)


urlpatterns = [
    path("clientes/", ClienteListView.as_view(), name="cliente-list"),
    path("clientes/nuevo/", ClienteCreateView.as_view(), name="cliente-create"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente-update"),
    path("clientes/<int:pk>/eliminar/", ClienteDeleteView.as_view(), name="cliente-delete"),
    path("transacciones/", TransaccionListView.as_view(), name="transaccion-list"),
    path("transacciones/nueva/", TransaccionCreateView.as_view(), name="transaccion-create"
),
]