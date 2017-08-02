from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

SALES_REPORT_TEMPLATE = 'templates/pdf/sales_report.html'
SALES_REPORT_STYLE = 'static/css/report_style.css'
OUTPUT_FOLDER = 'static/pdf/'

def generateSalesPdf(data):
	env = Environment(loader = FileSystemLoader('.'))
	template = env.get_template(SALES_REPORT_TEMPLATE)
	template_vars = data
	html_output = template.render(template_vars)
	HTML(string=html_output).write_pdf(OUTPUT_FOLDER + data['title'] + ".pdf")
