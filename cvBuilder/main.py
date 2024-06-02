# import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader
import pdfkit

# def extract_text_from_pdf(pdf_path):
#     document = fitz.open(pdf_path)
#     text = ""
#     for page_num in range(document.page_count):
#         page = document.load_page(page_num)
#         text += page.get_text()
#     return text

def render_cv_template(template_path, output_path, context):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    rendered_content = template.render(context)
    
    with open(output_path, 'w') as file:
        file.write(rendered_content)

def main():
    # pdf_path = 'your_cv.pdf'
    # cv_text = extract_text_from_pdf(pdf_path)

    context = {
    'name': 'Mateusz Podstawka',
    'phone': '+48 504 029 291',
    'email': 'mateusz.podstawka23@gmail.com',
    'location': 'Warsaw',
    'website': 'https://steadiercash.github.io',
    'linkedin': 'https://www.linkedin.com/in/mateusz-podstawka-146454210/',
    'github': 'https://github.com/SteadierCash',
    'experience': [
        {
            'company': 'Boś Bank',
            'location': 'Warsaw',
            'dates': 'July 2022 - Present',
            'title': 'Credit Risk Modeling Specialist',
            'description': 'Designing Python automation tools optimized for bank operations...'
        },
        {
            'company': 'Ministry of Finance',
            'location': 'Warsaw',
            'dates': 'July 2021 - September 2021',
            'title': 'Intern at the Process Robotization Center',
            'description': 'Conducting analysis of contractual terms...'
        }
    ],
    'education': [
        {
            'degree': 'Master\'s Degree',
            'institution': 'SGH Warsaw School of Economics',
            'dates': '2023 - Present'
        },
        {
            'degree': 'Bachelor\'s Degree',
            'institution': 'Warsaw University of Technology',
            'dates': '2019 - 2024'
        }
    ],
    'skills': {
        'programming': 'Python, Java, C++, C, SQL, HTML',
        'databases': 'Oracle, SQL server',
        'tools': 'Flask, Git, AWS, Azure, Linux',
        'soft': 'Adaptability, Problem-solving, Time management, Critical thinking',
        'languages': 'English - C1, Polish - Native'
    },
    'certifications': [
        'CS50’s Introduction to Computer Science - Harvard University',
        '100 Days of Code: The Complete Python Pro Bootcamp for 2023 - Udemy',
        'Java 17 Masterclass: Start Coding in 2024 - Udemy'
    ],
    'projects': [
        {
            'name': 'Eldoria Game',
            'description': 'A text-based adventure game written in Python...'
        },
        {
            'name': 'Job Offers Manager',
            'description': 'A C++ application tailored to simplify job offer management...'
        }
    ],
    'about_me': 'I\'m a first-year Master’s student deeply passionate about computer science...'
}


    render_cv_template('cvTemplate.html', 'output_cv.html', context)
    pdfkit.from_file('output_cv.html', 'output_cv.pdf')

if __name__ == "__main__":
    main()
