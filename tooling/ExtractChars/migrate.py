import os
import re
from bs4 import BeautifulSoup

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    page = "og.char.a-d.html"
    extracted = "extracted.char.a-d.html"
    html_path = os.path.join(script_dir, page)
    output_path = os.path.join(script_dir, extracted)
    print(f"Extracting '{html_path}' into '{output_path}'...")
    extract(html_path, output_path)
    print("Done!")

def extract(page: str, output: str):
    with open(page, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    tbody = soup.find("tbody")
    rows = []

    for tr in tbody.find_all("tr"):
        cols = [td.decode_contents() for td in tr.find_all("td")]
        rows.append(cols)

    html = ""
    for row in rows:
        content = row[1]
        character_id = extract_id(content)
        character_name = extract_name(content)
        character_description = extract_description(content)
        html = html + generate_html(character_id, character_name, character_description)
        
    with open(output, "w", encoding="utf-8") as output:
        output.write(html)
        
def extract_name(font_content: str) -> str:
    soup = BeautifulSoup(font_content, "html.parser")
    font = soup.find("font")
    b = font.find("b")
    full_name = b.get_text(" ", strip=True)
    clean_name_first_pass = full_name.replace("\n", "").replace("\r", "").strip()
    clean =  re.sub(r" +", " ", clean_name_first_pass)
    return clean

def extract_id(font_content: str):
    soup = BeautifulSoup(font_content, "html.parser")
    font = soup.find("font")
    b = font.find("b")
    a = b.find("a")
    name = a.get("name")

    # convert to CamelCase
    camel = "".join(word.capitalize() for word in name.split())
    return camel

def extract_description(html: str):
    soup = BeautifulSoup(html, "html.parser")
    font = soup.find("font")

    # find the first <br> inside the font tag
    br = font.find("br")
    if not br:
        return ""

    # collect all text that appears after the <br> tag
    text_parts = []
    for element in br.next_siblings:
        if isinstance(element, str):
            text_parts.append(element)
        else:
            text_parts.append(element.get_text(" ", strip=False))

    # join and clean whitespace
    raw = " ".join(text_parts)
    clean = " ".join(raw.split())  # collapse excessive whitespace

    return clean

def generate_html(id: str, name: str, description: str) -> str:
    return f"""    <br />
    <div id="{id}" class="ls-message">
                <div class="ls-content-faceset">
            <img class="ls-faceset" src="../../resources/characters/Unknown.png" alt="Faceset">
        </div>
        <div class="ls-content-header">
            <p>{name}</p>
        </div>
        <div class="ls-content-box">
            <p>{description}
            </p>
        </div>
    </div>"""


if __name__ == "__main__":
    main()
