"""
=====================================================================
 Calculadora de Margen de Ganancia
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_margen_ganancia_productos_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Calculadora de Margen de Ganancia."""

    def __init__(self, costo, precio):
        self.costo = float(costo)
        self.precio = float(precio)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.precio == 0:
            return {"error": "El precio no puede ser 0."}
        ganancia = self.precio - self.costo
        margen = ganancia / self.precio * 100
        markup = ganancia / self.costo * 100 if self.costo > 0 else 0
        return {"ganancia": ganancia, "margen": margen, "markup": markup}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["margen"] < 20:
            return "⚠️ Margen bajo (<20%). Revisa tus costos o sube el precio."
        return "✅ Margen saludable."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("costo"), input_float("precio"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">📈 Margen: {fmt_pct(r["margen"])}</div>
      <p class="result-detail">Ganancia: {fmt_moneda(r["ganancia"])} · Markup: {fmt_pct(r["markup"])}</p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "costo": input_float("costo"),
            "precio": input_float("precio"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "costo" in datos:
            document.querySelector("#costo").value = datos["costo"]
        if "precio" in datos:
            document.querySelector("#precio").value = datos["precio"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
