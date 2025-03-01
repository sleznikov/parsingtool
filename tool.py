# bring in LLAMA_CLOUD_API_KEY
from dotenv import load_dotenv
load_dotenv()
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader
import re
import sys
import textwrap

# Check if PDF path is provided as command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_pdf>")
    sys.exit(1)

pdf_path = sys.argv[1]

# set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# use SimpleDirectoryReader to parse the file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(input_files=[pdf_path], file_extractor=file_extractor).load_data()

# Get markdown content directly from documents
markdown_content = "\n\n".join(doc.text for doc in documents)

# Function to parse the markdown content
def parse_markdown(markdown_content):
    sections = []
    current_section = None
    current_subsection = None
    content_buffer = []

    # Regular expression to detect lines starting with a number followed by a period
    subsection_pattern = re.compile(r'^\d+\.\s+')

    for line in markdown_content.splitlines():
        if line.startswith('# ') and not line.strip().endswith('#'):
            if current_section and content_buffer:
                sections.append({'Section': current_section, 'Sub-Section': current_subsection or 'NA', 'Content': '\n'.join(content_buffer)})
                content_buffer = []
            current_section = line[2:].strip()
            current_subsection = None
        elif subsection_pattern.match(line):
            if current_section and content_buffer:
                sections.append({'Section': current_section, 'Sub-Section': current_subsection or 'NA', 'Content': '\n'.join(content_buffer)})
                content_buffer = []
            current_subsection = subsection_pattern.match(line).group(0).strip()
            content_buffer.append(line[len(current_subsection):].strip())
        elif line.strip().startswith("Instructions:"):
            if current_section and content_buffer:
                sections.append({'Section': current_section, 'Sub-Section': current_subsection or 'NA', 'Content': '\n'.join(content_buffer)})
                content_buffer = []
            current_section = line.strip()
            current_subsection = None
        elif line.strip() and current_section:
            content_buffer.append(line.strip())

    if current_section and content_buffer:
        sections.append({'Section': current_section, 'Sub-Section': current_subsection or 'NA', 'Content': '\n'.join(content_buffer)})

    return sections

# Function to print structured table to console
def print_structured_table(parsed_data):
    # Define column widths
    col1_width = 30
    col2_width = 15
    col3_width = 80
    
    # Print header
    print("STRUCTURED PDF DATA")
    print("=" * (col1_width + col2_width + col3_width + 6))
    print(f"{'Sections':<{col1_width}} | {'Sub-Sections':<{col2_width}} | {'Content':<{col3_width}}")
    print("-" * (col1_width + col2_width + col3_width + 6))

    # Print rows
    for entry in parsed_data:
        section = entry['Section'][:col1_width].ljust(col1_width)
        subsection = entry['Sub-Section'][:col2_width].ljust(col2_width)
        
        # Split content into lines
        content_lines = entry['Content'].split('\n')
        for i, line in enumerate(content_lines):
            # Wrap long lines to fit within col3_width
            wrapped_lines = textwrap.wrap(line, width=col3_width)
            if not wrapped_lines:  # Handle empty lines
                wrapped_lines = [""]
            
            # Print first wrapped line with section/subsection
            if i == 0:
                print(f"{section} | {subsection} | {wrapped_lines[0].ljust(col3_width)}")
            else:
                print(f"{' ' * col1_width} | {' ' * col2_width} | {wrapped_lines[0].ljust(col3_width)}")
            
            # Print any additional wrapped lines
            for wrapped_line in wrapped_lines[1:]:
                print(f"{' ' * col1_width} | {' ' * col2_width} | {wrapped_line.ljust(col3_width)}")

    print("=" * (col1_width + col2_width + col3_width + 6))

# Parse and display the content
parsed_data = parse_markdown(markdown_content)
print_structured_table(parsed_data)