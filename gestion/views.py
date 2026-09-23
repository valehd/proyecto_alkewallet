from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Cliente
from .models import Transaccion, Cuenta
from django.contrib.auth.mixins import LoginRequiredMixin


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "gestion/cliente_list.html"
    context_object_name = "clientes"


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ["nombre", "email", "telefono"]
    template_name = "gestion/cliente_form.html"
    success_url = reverse_lazy("cliente-list")
    def form_valid(self, form):

        response = super().form_valid(form)

        ultima_cuenta = Cuenta.objects.order_by("-id").first()

        if ultima_cuenta:
            siguiente_numero = ultima_cuenta.id + 1
        else:
            siguiente_numero = 1

        numero_cuenta = f"ALK{siguiente_numero:03d}"

        Cuenta.objects.create(
            cliente=self.object,
            numero_cuenta=numero_cuenta,
            saldo=0
        )

        return response


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ["nombre", "email", "telefono"]
    template_name = "gestion/cliente_form.html"
    success_url = reverse_lazy("cliente-list")


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "gestion/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente-list")


class TransaccionListView(LoginRequiredMixin, ListView):

    model = Transaccion

    template_name = "gestion/transaccion_list.html"

    context_object_name = "transacciones"

    def get_queryset(self):
        return Transaccion.objects.select_related(
            "cuenta",
            "cuenta__cliente"
        ).order_by("fecha", "id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        saldos = {}
        transacciones = []

        for transaccion in context["transacciones"]:

            cuenta_id = transaccion.cuenta.id

            if cuenta_id not in saldos:
                saldos[cuenta_id] = 0

            if transaccion.tipo == "INGRESO":
                saldos[cuenta_id] += transaccion.monto

            elif transaccion.tipo == "RETIRO":
                saldos[cuenta_id] -= transaccion.monto

            transaccion.saldo_despues = saldos[cuenta_id]

            transacciones.append(transaccion)

        context["transacciones"] = transacciones

        return context

class TransaccionCreateView(LoginRequiredMixin, CreateView):

    model = Transaccion

    fields = ["cuenta", "tipo", "monto", "descripcion", "etiquetas"]

    template_name = "gestion/transaccion_form.html"

    success_url = reverse_lazy("transaccion-list")

    def form_valid(self, form):

        transaccion = form.save(commit=False)
        cuenta = transaccion.cuenta

        if transaccion.tipo == "INGRESO":
            cuenta.saldo += transaccion.monto

        elif transaccion.tipo == "RETIRO":

            if transaccion.monto > cuenta.saldo:
                form.add_error(
                    "monto",
                    "El saldo de la cuenta es insuficiente para realizar este retiro."
                )
                return self.form_invalid(form)

            cuenta.saldo -= transaccion.monto

        cuenta.save()
        transaccion.save()
        form.save_m2m()

        return super().form_valid(form)