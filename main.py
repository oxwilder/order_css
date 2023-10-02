import sys
import os
import tinycss2
from cssselect import parse

def calculate_specificity(selector):
    return parse(selector)[0].specificity()

def sort_rules(css_text):
    rules = tinycss2.parse_stylesheet(css_text, skip_comments=True, skip_whitespace=True)
    rule_data = []
    for rule in rules:
        if rule.type == 'qualified-rule':
            selector = tinycss2.serialize(rule.prelude)
            body = tinycss2.serialize(rule.content)
            specificity = calculate_specificity(selector)
            rule_data.append((specificity, selector, body))
    
    sorted_rules = sorted(rule_data)
    sorted_css = ''
    for specificity, selector, body in sorted_rules:
        sorted_css += f"{selector} {{{body}}}\n"
    return sorted_css

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <css_file_name>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    with open(input_file, 'r') as file:
        css_text = file.read()

    sorted_css = sort_rules(css_text)

    # Construct output file name
    file_root, file_ext = os.path.splitext(input_file)
    output_file = f"{file_root}-reordered{file_ext}"

    with open(output_file, 'w') as file:
        file.write(sorted_css)

    print(f"Sorted CSS written to: {output_file}")

if __name__ == "__main__":
    main()
