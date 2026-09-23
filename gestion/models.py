from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import transaction


# Modelos
# Un cliente tiene una cuenta (OneToOne).
# Una cuenta puede tener muchas transacciones (FK)
# Una transaccion puede tener varias etiquetas(alimentacion, entretenimiento, salud,etc) y una etiqueta puede utilizarse en muchas transacciones (ManyToMany).



class Cliente(models.Model):
    nombre= models.CharField(max_length=100)
    email= models.EmailField(unique=True)
    telefono= models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    cliente=models.OneToOneField(Cliente, on_delete=models.CASCADE,related_name="cuenta")
    numero_cuenta=models.CharField(max_length=20, unique=True)
    saldo=models.DecimalField(max_digits=12,decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.numero_cuenta


class Etiqueta(models.Model):
    nombre=models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name="transacciones"
    )

    etiquetas = models.ManyToManyField(
        Etiqueta,
        blank=True,
        related_name="transacciones"
    )

    tipo = models.CharField(
        max_length=20,
        choices=[
            ("INGRESO", "Ingreso"),
            ("RETIRO", "Retiro"),
        ]
    )

    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    fecha = models.DateTimeField(auto_now_add=True)

    descripcion = models.CharField(max_length=200, blank=True)

    def clean(self):
        super().clean()

        if self.tipo == "RETIRO" and self.cuenta.saldo < self.monto:
            raise ValidationError(
                {"monto": "Saldo insuficiente para realizar el retiro."}
            )

    @transaction.atomic
    def save(self, *args, **kwargs):
        nueva = self.pk is None

        self.full_clean()

        super().save(*args, **kwargs)

        if nueva:
            if self.tipo == "INGRESO":
                self.cuenta.saldo += self.monto
            else:
                self.cuenta.saldo -= self.monto

            self.cuenta.save(update_fields=["saldo"])

    def __str__(self):
        return f"{self.tipo} - {self.monto}"