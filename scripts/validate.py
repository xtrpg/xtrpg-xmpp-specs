import sys
from pathlib import Path
from lxml import etree

def validate_xml(xml_path, xsd_path):
    try:
        schema_doc = etree.parse(str(xsd_path))
        xml_schema = etree.XMLSchema(schema_doc)
        xml_doc = etree.parse(str(xml_path))
        
        xml_schema.assertValid(xml_doc)
        return True
    except Exception:
        return False

def main():
    schemas_dir = Path("schemas")
    examples_dir = Path("examples")
    
    if not schemas_dir.exists():
        print(f"Error: '{schemas_dir}' directory not found.", file=sys.stderr)
        sys.exit(1)

    report = []
    all_passed = True

    # Loop over all XSD files directly under the schemas/ folder
    for xsd_path in sorted(schemas_dir.glob("*.xsd")):
        schema_name = xsd_path.stem
        
        # Add the schema header to the report
        report.append(f"**{schema_name}.xsd**")
        
        # Corresponding folder under examples/
        xml_folder = examples_dir / schema_name
        
        # Find all XML files in the corresponding examples folder
        xml_files = sorted(xml_folder.glob("*.xml")) if xml_folder.exists() else []
        
        if not xml_files:
            report.append("- *No example files found*")
            report.append("") # Add empty line for spacing
            continue
            
        for xml_path in xml_files:
            passed = validate_xml(xml_path, xsd_path)
            status_icon = "✅" if passed else "⛔"
            
            if not passed:
                all_passed = False
                
            report.append(f"- {status_icon} {xml_path.name}")
        
        report.append("") # Add empty line for spacing between schemas

    # Print the final Markdown report
    print("\n".join(report))

    # Exit with appropriate code if any validation failed
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()