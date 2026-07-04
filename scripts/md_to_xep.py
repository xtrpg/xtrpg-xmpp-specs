import sys
import re
import yaml
from html.parser import HTMLParser

class XsfStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.stack = []  # Tracks currently open section levels: e.g., [1, 2]

    def close_sections_to_level(self, level):
        """Closes any open sections that are at or deeper than the incoming level."""
        while self.stack and self.stack[-1] >= level:
            closed_level = self.stack.pop()
            self.output.append(f"\n</section{closed_level}>")

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # Check if it's a header tag from h2 to h6
        match = re.match(r'^h([2-6])$', tag)
        if match:
            header_num = int(match.group(1))
            section_level = header_num - 1

            # 1. Close any open sections that have a number >= current section level
            self.close_sections_to_level(section_level)

            # 2. Open the new section container
            self.stack.append(section_level)

            anchor_str = f" anchor='{attr_dict['id']}'" if 'id' in attr_dict else ""
            self.output.append(f"\n<section{section_level} topic='")

            # Set internal flag so we know we are capturing the header's text/topic
            self.in_header = True
            self.current_anchor_str = anchor_str
            return

        # Handle standard tags (like <p>)
        self.in_header = False
        attr_str = "".join([f" {k}='{v}'" for k, v in attrs.items()])
        self.output.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        match = re.match(r'^h([2-6])$', tag)
        if match:
            # We finished capturing the header text, finish opening the container
            self.output.append(f"'{self.current_anchor_str}>")
            self.in_header = False
            return

        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        # Pass text directly through
        self.output.append(data)

    def close_all(self):
        """Closes any remaining open sections at the end of the document."""
        while self.stack:
            closed_level = self.stack.pop()
            self.output.append(f"\n</section{closed_level}>")


def convert_md_to_xsf(html_content, yaml_metadata):
    # 1. Pull values from the parsed front matter dictionary
    title = yaml_metadata.get('Title', 'Untitled XEP Extension')
    abstract = yaml_metadata.get('Abstract', 'No abstract provided.')
    status = yaml_metadata.get('Status', 'Experimental')
    type = yaml_metadata.get('Type', 'Standards Track')
    number = yaml_metadata.get('Number', 'XXXX')

    # 2. Parse flat HTML hierarchy into nested XSF sections
    parser = XsfStructureParser()
    parser.feed(html_content)
    parser.close_all()
    processed = "".join(parser.output)

    # Convert code blocks to XSF example blocks
    processed = re.sub(
        r'<pre><code class="language-xml">(.*?)</code></pre>',
        r'<example><![CDATA[\1]]></example>',
        processed,
        flags=re.DOTALL
    )

    # 3. Inject metadata and content into the XSF structural boilerplate
    xsf_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE xep SYSTEM 'xep.dtd'>
<xep>
  <header>
    <title>{title}</title>
    <abstract>{abstract}</abstract>
    <number>{number}</number>
    <status>{status}</status>
    <type>{type}</type>
    <sig>Standards</sig>
  </header>
  <itemtype>Feature</itemtype>
  <body>
    {processed}
  </body>
</xep>"""
    return xsf_xml

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python md_to_xep.py <input_html> <original_md>")
        sys.exit(1)

    html_file = sys.argv[1]
    md_file = sys.argv[2]

    # Read and parse the front matter from the original markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    # Extract the YAML block between the triple-dashes
    yaml_metadata = {}
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw_md, re.DOTALL)
    if yaml_match:
        yaml_metadata = yaml.safe_load(yaml_match.group(1))

    # Read the Pandoc-generated HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(convert_md_to_xsf(html_content, yaml_metadata))
