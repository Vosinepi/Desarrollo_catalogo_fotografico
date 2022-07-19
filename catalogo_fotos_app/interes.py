import math

interes = float(38.6)
interes2 = 38
print(f"interes plazo fijo {interes} %")
interes_diario = interes / 365
print(f"interes diario {interes_diario}")
plata = 32744
tiempo = 7
monto = math.pow(1.0 + interes_diario / 100, tiempo) * plata
print(f"plata {plata}")

print(f"Plata por dia {(plata * (1.0 + interes_diario / 100))-plata}")
print(f" en una semana {monto - plata}")
