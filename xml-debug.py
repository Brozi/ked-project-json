import xml.dom.minidom as md
import json

json_content = """
{
  "id": 101,
  "imie": "Jan",
  "nazwisko": "Kowalski",
  "wiek": 34,
  "email": "jan.kowalski@example.com",
  "aktywny": true,
  "rola": "administrator",
  "zainteresowania": ["programowanie", "rower", "góry"],
  "adres": {
    "miasto": "Kraków",
    "ulica": "Floriańska",
    "kod_pocztowy": "31-019"
  },
  "data_rejestracji": "2023-05-12T10:30:00Z"
}
"""

json_dict = json.loads(json_content)

doc = md.Document()
root = doc.createElement("root")
doc.appendChild(root)


def create_tag(name, value, parent):
    def create_tags(tags, i_parent):
        for number, value in enumerate(tags):
            if type(value) == dict:
                create_tag(f"tag_{number}", value, i_parent)
                continue
                i_tag = doc.createElement(f"tag_{number}")
                i_parent.appendChild(i_tag)
                if type(value) == list:
                    create_tags(value, i_tag)
                else:
                    i_content = doc.createTextNode(str(value))
                    i_tag.appendChild(i_content)

    tag = doc.createElement(name)
    parent.appendChild(tag)
    if type(value) == dict:
        for v_key, v_value in value.items():
            create_tag(v_key, v_value, tag)
    elif type(value) == list:
        create_tags(value, "list_content")
        for list_value in value:
            create_tag("list_content", list_value, tag)

    else:
        content = doc.createTextNode(str(value))
        tag.appendChild(content)


for key, val in json_dict.items():
    create_tag(key, val, root)
print(doc.toprettyxml())
with open("output.xml", "w", encoding="utf-8") as f:
    doc.writexml(f, addindent="\t", newl="\n")