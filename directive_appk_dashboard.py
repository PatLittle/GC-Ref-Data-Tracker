import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def count_links_in_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.count('](')
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return 0


def count_entries_on_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='table-responsive2').find('table')
        if table:
            rows = table.find_all('tr')
            return len(rows) - 1
        else:
            print(f"No table found on page: {url}")
            return 0
    except Exception as e:
        print(f"Error fetching entries from {url}: {e}")
        return 0


def generate_markdown_files():
    urls = [
        ('https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601#appK', 'docs/directive_appendix_k_eng.md'),
        ('https://www.tbs-sct.canada.ca/pol/doc-fra.aspx?id=32601#appK', 'docs/directive_appendix_k_fra.md')
    ]
    for url, output_file in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            directive_content = soup.find('h2', id='appK').find_parent('details')
            if directive_content:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(directive_content.prettify())
                print(f"Saved {output_file}")
            else:
                print(f"Directive content not found at {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")


def append_to_csv(date, status, en_appk, en_canadaca, fr_appk, fr_canadaca):
    csv_file = 'docs/chart_data.csv'
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # Write headers if file is empty
                writer.writerow(['date', 'status', 'EN_AppK', 'EN_Canadaca', 'FR_AppK', 'FR_Canadaca'])
            writer.writerow([date, status, en_appk, en_canadaca, fr_appk, fr_canadaca])
        print(f"Appended data to {csv_file}")
    except Exception as e:
        print(f"Error appending to CSV: {e}")


def generate_bar_chart_widget(markdown_files, reference_pages):
    data = []
    labels = ['ENGLISH', 'FRENCH']
    markdown_links = []
    page_entries = []
    colors_md = []
    colors_entries = []
    all_equal = True

    for file, page in zip(markdown_files, reference_pages):
        md_links = count_links_in_markdown(file)
        entries = count_entries_on_page(page)
        markdown_links.append(md_links)
        page_entries.append(entries)
        if md_links == entries:
            colors_md.append('green')
            colors_entries.append('green')
        else:
            all_equal = False
            if md_links < entries:
                colors_md.append('red')
                colors_entries.append('darkgrey')
            else:
                colors_md.append('darkgrey')
                colors_entries.append('red')

    chart_title = "✅Directive on Service and Digital: Appendix K updated 🆗" if all_equal else "🚩Directive on Service and Digital: Appendix K not updated 🆖"

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            .chart-container {{
                width: 80%;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <h1>{chart_title}</h1>
        <div class="chart-container">
            <canvas id="barChart"></canvas>
        </div>
        <script>
            const ctx = document.getElementById('barChart').getContext('2d');
            const chart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels},
                    datasets: [
                        {{
                            label: 'Count DRS in AppK',
                            data: {markdown_links},
                            backgroundColor: {colors_md},
                            borderColor: 'black',
                            borderWidth: 2
                        }},
                        {{
                            label: 'Count DRS on Canada.ca',
                            data: {page_entries},
                            backgroundColor: {colors_entries},
                            borderColor: 'black',
                            borderWidth: 2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        tooltip: {{
                            callbacks: {{
                                label: function(tooltipItem) {{
                                    return tooltipItem.dataset.label + ": " + tooltipItem.raw;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            stacked: false
                        }},
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: 'Count'
                            }}
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    '''

    with open('docs/bar_chart_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Bar chart dashboard saved to docs/bar_chart_dashboard.html")

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = chart_title.split(':')[1].strip()
    append_to_csv(now, status, markdown_links[0], page_entries[0], markdown_links[1], page_entries[1])


if __name__ == "__main__":
    generate_markdown_files()
    markdown_files = [
        'docs/directive_appendix_k_eng.md',
        'docs/directive_appendix_k_fra.md'
    ]
    reference_pages = [
        'https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html',
        'https://www.canada.ca/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc.html'
    ]
    generate_bar_chart_widget(markdown_files, reference_pages)
