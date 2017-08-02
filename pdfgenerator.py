from jinja2 import Environment, FileSystemLoader

SALES_REPORT_TEMPLATE = 'templates/pdf/sales_report.html'

def generateSalesPdf(data):
	env = Environment(loader = FileSystemLoader('.'))
	template = env.get_template(SALES_REPORT_TEMPLATE)
	template_vars = data
	html_output = template.render(template_vars)
	print (html_output)

