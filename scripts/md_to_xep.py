import sys
import re
import yaml

def convert_md_to_xsf(html_content, yaml_metadata):
    # 1. Pull values from the parsed front matter dictionary
    title = yaml_metadata.get('Title', 'Untitled XEP Extension')
    abstract = yaml_metadata.get('Abstract', 'No abstract provided.')

    # 2. Map standard markdown/HTML structures to XSF layout tags
    processed = re.sub(r'<h2>(.*?)</h2>', r"<section1 topic='\1'>", html_content)
    processed = re.sub(r'<h3>(.*?)</h3>', r"<section2 topic='\1'>", processed)

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
    <status>Experimental</status>
    <type>Standards Track</type>
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
