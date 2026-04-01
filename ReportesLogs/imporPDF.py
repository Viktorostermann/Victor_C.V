from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# Registrar varias variantes
pdf.add_font("DejaVu", "", r"C:\Proyectos\Project_Manager\Victor_C.V\ReportesLogs\fonts\DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", r"C:\Proyectos\Project_Manager\Victor_C.V\ReportesLogs\fonts\DejaVuSans-Bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", r"C:\Proyectos\Project_Manager\Victor_C.V\ReportesLogs\fonts\DejaVuSans-Oblique.ttf", uni=True)

# Usar la fuente
pdf.set_font("DejaVu", size=12)
pdf.cell(200, 10, "Texto con Unicode → ✓ áéíóú", ln=True)

pdf.output("reporte.pdf")
