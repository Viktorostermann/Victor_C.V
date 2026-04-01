import os
import sys
import platform
import logging
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos


# Ruta central del log
LOG_PATH = r"C:\Proyectos\Project_Manager\Logs_Environment\auto_General.log"

# Configuración del logger (ampliada)
logging.basicConfig(
    filename=LOG_PATH,                # ruta central del log
    filemode="a",                     # "a" agrega al final, "w" sobrescribe
    format="%(asctime)s - %(levelname)s - %(message)s",  # formato de salida
    level=logging.DEBUG               # nivel mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

# Ejemplo de uso
logging.info("Información general")
logging.info("Aplicación iniciada")
logging.warning("Advertencia: recurso no encontrado")
logging.error("Error crítico en el proceso")
logging.critical("Error crítico en el sistema")
logging.debug("Información de depuración")

# Función para simular consultas a motores de IA externos
def consultar_ia(mensaje):
    sugerencias = []
    sugerencias.append(f"Copilot sugiere revisar dependencias relacionadas con: {mensaje}")
    sugerencias.append(f"ChatGPT recomienda verificar permisos de archivos o procesos para: {mensaje}")
    sugerencias.append(f"Gemini aconseja actualizar librerías o frameworks vinculados a: {mensaje}")
    sugerencias.append(f"OpenCloud indica revisar configuración del entorno para: {mensaje}")
    return sugerencias

# Procesamiento del registro de logs
def procesar_log(filepath):
    registros = []
    if not os.path.isfile(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("INFO: Archivo de log creado automáticamente.\n")

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            texto = linea.strip()
            if not texto:
                continue

            criticidad = "Log"
            solucion = "Entrada registrada automáticamente. Revisar si requiere acción."
            soluciones_posibles = []
            codigo_error = 0

            if "Error" in texto or "ERROR" in texto:
                criticidad = "Error"
                solucion = "Revisar el mensaje y aplicar corrección según contexto."
                soluciones_posibles.append("Verificar dependencias, permisos o sintaxis según el error.")
                soluciones_posibles.extend(consultar_ia(texto))
                codigo_error = 1

            elif "Warning" in texto or "WARNING" in texto:
                criticidad = "Warning"
                solucion = "Verificar si el warning afecta la ejecución o puede ignorarse."
                soluciones_posibles.append("Actualizar librerías o revisar configuración.")
                soluciones_posibles.extend(consultar_ia(texto))
                codigo_error = 2

            elif texto.startswith("[LANGUAGE-FORCE]"):
                criticidad = "Info"
                solucion = "Registro de detección/forzado de lenguajes y frameworks. No requiere acción."
                codigo_error = 100

            elif texto.startswith("[ISSUE-IGN]"):
                criticidad = "Auditoría"
                solucion = "Chequeos de seguridad reactivados o ignorados. Revisar si corresponde mantener la decisión."
                codigo_error = 200

            elif texto.startswith("[GLF]"):
                criticidad = "Info"
                solucion = "Forzado de lenguajes aplicado a archivos. No requiere acción."
                codigo_error = 101

            elif texto.startswith("[IGN]"):
                criticidad = "Ignorado"
                solucion = "Archivo o recurso excluido de estadísticas. No requiere acción."
                codigo_error = 300

            registros.append({
                "dia": datetime.now().strftime("%A"),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "criticidad": criticidad,
                "codigo_error": codigo_error,
                "porque_falla": texto,
                "solucion": solucion,
                "soluciones_posibles": soluciones_posibles,
                "direccion_registro_afectado": filepath,
                "aplicacion_origen": os.path.basename(sys.argv[0]),
                "entorno_ejecucion": "Visual Studio Code",
                "sistema_operativo": platform.system() + " " + platform.release()
            })

    return registros   # ← ahora siempre devuelve lista

# Exportación a MD
def exportar_md(registros, outdir):
    md_path = os.path.join(outdir, "reporte.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 📋 Reporte Global de Logs - PokedexPersonal\n\n")
        for r in registros:
            f.write(f"---\n\n")
            f.write(f"⚠ Criticidad: {r['criticidad']}\n")
            f.write(f"🔢 Código de error: {r['codigo_error']}\n")
            f.write(f"📝 Mensaje: {r['porque_falla']}\n")
            f.write(f"📅 Día: {r['dia']}\n")
            f.write(f"⏰ Fecha: {r['fecha']}\n")
            f.write(f"✅ Solución específica: {r['solucion']}\n")
            f.write(f"📂 Dirección registro afectado: {r['direccion_registro_afectado']}\n")
            f.write(f"🖥 Aplicación origen: {r['aplicacion_origen']}\n")
            f.write(f"🛠 Entorno de ejecución: {r['entorno_ejecucion']}\n")
            f.write(f"💻 Sistema operativo: {r['sistema_operativo']}\n\n")
            if r.get("soluciones_posibles"):
                f.write("🤖 Sugerencias IA:\n")
                for s in r["soluciones_posibles"]:
                    f.write(f"- {s}\n")
            f.write("\n\n")
    return md_path

# Exportación a HTML
def exportar_html(registros, outdir):
    html_path = os.path.join(outdir, "reporte.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>Reporte Global de Logs - PokedexPersonal</h1>")
        for r in registros:
            f.write("<div style='margin-bottom:20px; text-align:left;'>")
            f.write(f"<p>⚠ <b>Criticidad:</b> {r['criticidad']}<br>")
            f.write(f"🔢 <b>Código de error:</b> {r['codigo_error']}<br>")
            f.write(f"📝 <b>Mensaje:</b> {r['porque_falla']}<br>")
            f.write(f"📅 <b>Día:</b> {r['dia']}<br>")
            f.write(f"⏰ <b>Fecha:</b> {r['fecha']}<br>")
            f.write(f"✅ <b>Solución específica:</b> {r['solucion']}<br>")
            f.write(f"📂 <b>Dirección registro afectado:</b> {r['direccion_registro_afectado']}<br>")
            f.write(f"🖥 <b>Aplicación origen:</b> {r['aplicacion_origen']}<br>")
            f.write(f"🛠 <b>Entorno de ejecución:</b> {r['entorno_ejecucion']}<br>")
            f.write(f"💻 <b>Sistema operativo:</b> {r['sistema_operativo']}<br>")
            if r.get("soluciones_posibles"):
                f.write("🤖 <b>Sugerencias IA:</b><br>")
                for s in r["soluciones_posibles"]:
                    f.write(f"- {s}<br>")
            f.write("</p></div>")
        f.write("</body></html>")
    return html_path


    # Exportación del registro  a formato PDF

def exportar_pdf(registros, outdir):
    pdf = FPDF()
    pdf.add_page()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(base_dir, "fonts")

    pdf.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"))
    pdf.set_font("DejaVu", size=11)

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font("DejaVu", size=14)
    pdf.cell(page_width, 12, "Reporte Global de Logs - PokedexPersonal ✓",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    for idx, r in enumerate(registros, start=1):
        pdf.set_font("DejaVu", size=12)
        pdf.set_text_color(0, 0, 128)
        pdf.cell(page_width, 10, f"Registro #{idx}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("DejaVu", size=11)
        safe_text = r['porque_falla'].replace("\n", " ").replace("\r", " ")

        # Colorear según criticidad
        if r['criticidad'] == "Error":
            pdf.set_text_color(200, 0, 0)
        elif r['criticidad'] == "Warning":
            pdf.set_text_color(255, 140, 0)
        elif r['criticidad'] == "Info":
            pdf.set_text_color(100, 100, 100)
        else:
            pdf.set_text_color(0, 0, 0)

        # Bloque principal
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"⚠ Criticidad: {r['criticidad']}", align="L")
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"🔢 Código de error: {r['codigo_error']}", align="L")
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"📝 Mensaje: {safe_text}", align="L")
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"📅 Día: {r['dia']}", align="L")
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"⏰ Fecha: {r['fecha']}", align="L")

        pdf.set_text_color(0, 128, 0)
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"✅ Solución específica (sistema): {r['solucion']}", align="L")
        pdf.set_text_color(0, 0, 0)

        # Dirección registro afectado
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"📂 Dirección registro afectado: {r['direccion_registro_afectado']}", align="L")

        # Aplicación origen
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"🖥 Aplicación origen: {r['aplicacion_origen']}", align="L")

        # Entorno y sistema operativo
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"🛠 Entorno de ejecución: {r['entorno_ejecucion']}", align="L")
        pdf.set_x(pdf.l_margin + 5)
        pdf.multi_cell(page_width - 5, 8, f"💻 Sistema operativo: {r['sistema_operativo']}", align="L")

        # Sugerencias IA
        if r.get("soluciones_posibles"):
            pdf.ln(3)
            pdf.set_text_color(128, 0, 128)
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(page_width - 5, 8, "🤖 Sugerencias IA:", align="L")
            pdf.set_text_color(0, 0, 0)
            for s in r["soluciones_posibles"]:
                safe_s = s.replace("\n", " ").replace("\r", " ")
                pdf.set_x(pdf.l_margin + 10)
                pdf.multi_cell(page_width - 10, 8, f"• {safe_s}", align="L")

            pdf.set_x(pdf.l_margin + 5)

        # Separador visual
        pdf.ln(5)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(5)

    pdf_path = os.path.join(outdir, "reporte.pdf")
    pdf.output(pdf_path)
    print(f"Reporte generado en: {pdf_path}")

    # Bloque de apertura automática (comentado para evitar múltiples ventanas)
    """
    try:
        if sys.platform.startswith("win"):
            os.startfile(pdf_path)
        elif sys.platform.startswith("darwin"):
            os.system(f"open \"{pdf_path}\"")
        else:
            os.system(f"xdg-open \"{pdf_path}\"")
    except Exception as e:
        print(f"No se pudo abrir el archivo automáticamente: {e}")
    """

    return pdf_path




# -------------------------------- MAIN --------------------------------------------------------- #
if __name__ == "__main__":
    if len(sys.argv) < 3:
        DEFAULT_LOG = input("📂 Ingresa la ruta del archivo de log: ").strip()
        DEFAULT_OUTDIR = input("📂 Ingresa la carpeta de salida para el reporte: ").strip()
        DEFAULT_FORMAT = input("📄 Ingresa el formato (pdf/html/md) [pdf]: ").strip() or "pdf"
    else:
        DEFAULT_LOG = sys.argv[1]
        DEFAULT_OUTDIR = sys.argv[2]
        DEFAULT_FORMAT = sys.argv[3] if len(sys.argv) > 3 else "pdf"

    # 🔹 Crear carpeta de salida si no existe
    os.makedirs(DEFAULT_OUTDIR, exist_ok=True)

    registros = procesar_log(DEFAULT_LOG)

    if DEFAULT_FORMAT == "md":
        path = exportar_md(registros, DEFAULT_OUTDIR)
    elif DEFAULT_FORMAT == "html":
        path = exportar_html(registros, DEFAULT_OUTDIR)
    elif DEFAULT_FORMAT == "pdf":
        path = exportar_pdf(registros, DEFAULT_OUTDIR)
    else:
        print("Formato no válido. Usa md, html o pdf.")
        sys.exit(1)

    print(f"✅ Reporte generado en: {path}")


'''
🔹 Cómo funciona:

1- Ejecutas tu programa desde cualquiera de las consolas (CMD, PowerShell, Bash).
2- La salida se guarda en salida.log.
3- Llamas al script Python (procesar_logs.py).
4- El script analiza el log, genera un árbol problema → solución, y exporta Markdown, HTML y PDF en el directorio que elijas.
5- Cada registro tiene encabezado: Día, Fecha, Criticidad, Por qué falla, Solución, y dos saltos de línea entre registros.

✅ Con esto tienes un flujo global que funciona en todas las consolas.

'''