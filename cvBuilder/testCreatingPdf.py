import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def create_plot():
    # Create a simple plot and save it as an image
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')
    plot_filename = 'plot.png'
    plt.savefig(plot_filename)
    plt.close()
    return plot_filename

def create_table():
    # Create a sample dataframe
    data = {
        'Column 1': [1, 2, 3, 4],
        'Column 2': [1, 4, 9, 16],
        'Column 3': ['A', 'B', 'C', 'D']
    }
    df = pd.DataFrame(data)
    return df

def create_pdf(report_filename, plot_filename, table_data, text):
    # Create a PDF document
    doc = SimpleDocTemplate(report_filename, pagesize=letter)
    elements = []

    # Add text
    styles = getSampleStyleSheet()
    paragraph = Paragraph(text, styles['Normal'])
    elements.append(paragraph)
    elements.append(Spacer(1, 12))  # Add space after the paragraph
    
    # Add the plot image
    elements.append(Image(plot_filename, width=400, height=300))
    elements.append(Spacer(1, 12))  # Add space after the image

    # Create and add a table
    table_data = [table_data.columns.to_list()] + table_data.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)

# Parameters for the report
plot_filename = create_plot()
table_data = create_table()
text = 'This is a PDF report with a plot, table, and some text.'

# Create the PDF
create_pdf('automated_report.pdf', plot_filename, table_data, text)
