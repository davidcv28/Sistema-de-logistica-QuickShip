# QuickShip - Mi Proyecto de Gestión Logística

Este es un sistema que armé para manejar todo el proceso de envíos: desde que el usuario carga sus datos y cotiza, hasta que confirma el pedido y se genera el seguimiento. Lo desarrollé usando **Django** y **DRF**, y me enfoqué en separar todo por dominios para que el código sea limpio y fácil de mantener.

## 🚀 ¿Qué hace la App?

### 1. Usuarios y Perfiles "Inteligentes"
 El sistema valida:
*   **Datos reales de Argentina:** Metí lógica para validar DNI y CUIT/CUIL.
*   **Temas fiscales:** Según la condición de IVA del usuario (si es Monotributista o Responsable Inscripto), el sistema le exige la Razón Social y el CUIT automáticamente.
*   **Direcciones normalizadas:** Usé una base de provincias y ciudades para que no haya errores al cargar domicilios.

### 2. Borradores y Cotización (`PendingShipment`)
Antes de confirmar el envío, el usuario puede armar un borrador:
*   **Peso Volumétrico:** Programé un cálculo que compara el peso real contra el tamaño del paquete (alto x largo x ancho). El sistema elige el mayor para calcular el precio, que es como se maneja en la logística real.
*   **Lógica de precios:** Centralicé todo en clases de cálculo para que sea fácil cambiar las tarifas o el divisor volumétrico si hace falta.

### 3. Envíos y Seguimiento
Cuando el usuario confirma, el borrador se convierte en un envío real:
*   **Resguardo de datos (Snapshots):** Si el usuario cambia su dirección de perfil mañana, el envío que ya hizo hoy mantiene los datos originales. Esto lo hice para no perder la trazabilidad histórica.
*   **Tracking:** Genero códigos de seguimiento únicos para cada pedido.

## 🛠️ Cómo lo pensé técnicamente

*   **Seguridad en la DB:** Usé transacciones atómicas (`transaction.atomic`) para que, si algo falla al crear un envío, no se guarden datos a medias. También usé `RESTRICT` en las claves foráneas para no borrar provincias o ciudades que ya tienen envíos asociados.
*   **Código Limpio:** Saqué las validaciones pesadas de los serializadores y las puse en archivos `validator.py` y `mixins`. Así el código es mucho más fácil de leer.
*   **Arquitectura por Dominios:** En vez de tener archivos gigantes, dividí todo en carpetas por "tema" (`user`, `shipping`, `prices`). Es más organizado para trabajar.

## 🔧 Instalación rápida

1. **Cloná el repo:**
   ```bash
   git clone <url-del-repositorio>
   ```
2. **Armá tu entorno virtual:**
   ```bash
   python -v env venv
   source venv/bin/scripts/activate  # En Windows: .\venv\Scripts\activate
   ```
3. **Bajate las librerías:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Corré las migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---
**Proyecto desarrollado por mí, enfocado en resolver problemas reales de logística.**
```



