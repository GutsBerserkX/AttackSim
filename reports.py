from fpdf import fpdf


# Clase que representa el informe de los ataques
class Report:
    def __init__(self, attack_results: str, impact_analysis: str):
        """Inicializa el informe con los resultados del ataque y el análisis de impacto"""
        self.attack_results = attack_results
        self.impact_analysis = impact_analysis

    def display_report(self):
        """Muestra el informe en consola"""
        print("=== Informe del Ataque ===")
        print("Resultados del ataque:")
        print(self.attack_results)
        print("\nAnálisis de impacto:")
        print(self.impact_analysis)

    def generate_pdf(self, filename: str):
        """Genera un informe en formato PDF usando los resultados del ataque y el análisis de impacto"""
        pdf = fpdf()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Agregar el título del informe
        pdf.cell(200, 10, txt="Informe del Ataque", ln=True, align='C')

        # Agregar los resultados del ataque
        pdf.cell(200, 10, txt="Resultados del ataque:", ln=True, align='L')
        pdf.multi_cell(0, 10, txt=self.attack_results)

        # Agregar el análisis de impacto
        pdf.cell(200, 10, txt="\nAnálisis de impacto:", ln=True, align='L')
        pdf.multi_cell(0, 10, txt=self.impact_analysis)

        # Guardar el archivo PDF
        pdf.output(filename)
        print(f"Informe guardado como {filename}")
