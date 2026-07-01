import sys
from lxml import etree

def validate_xml(xml_path, xsd_path):
    try:
        schema_doc = etree.parse(xsd_path)
        xml_schema = etree.XMLSchema(schema_doc)
        xml_doc = etree.parse(xml_path)
        
        xml_schema.assertValid(xml_doc)
        print(f"✅ {xml_path} is valid against {xsd_path}")
        return True
    except Exception as e:
        print(f"❌ Validation failed for {xml_path}: {e}")
        return False

if __name__ == '__main__':
    # Quickly test our XEP-1 setup
    success = validate_xml("examples/rules-engine/valid-roll-request.xml", "schemas/rules-engine.xsd")
    sys.exit(0 if success else 1)