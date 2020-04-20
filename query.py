import requests
import csv
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

prefix_url = "http://purl.obolibrary.org/obo/cto#"


with open('annotation-properties.csv', mode='r') as csv_file, \
        open('annotation-prop-map.csv', 'w', newline='') as write_obj:
    csv_reader = csv.DictReader(csv_file)
    field_names = csv_reader.fieldnames+["NCBITAXON", "MESH", "Wikipedia"]
    csv_writer = csv.DictWriter(write_obj, field_names)
    csv_writer.writeheader()
    for row in csv_reader:
        if row["Annotation"].startswith(prefix_url):
            name = row["Annotation"][len(prefix_url):].replace("_", " ")
            print(name)

            url = "http://data.bioontology.org/search"
            params = {"q": name,
                      "exact_match": "true",
                      "ontologies": "NCBITAXON"
                      }

            hdr = {"Authorization": "apikey token=082a4703-4c2e-43fa-a25e-87eca91a9a1b"}

            r = requests.get(url, params=params, headers=hdr)

            resp_json = r.json()
            sa_ncbi = ""
            if resp_json["collection"]:
                sa_ncbi = resp_json["collection"][0]["@id"]

            params["ontologies"] = "MESH"
            r = requests.get(url, params=params, headers=hdr)
            resp_json = r.json()
            sa_mesh = ""
            if resp_json["collection"]:
                sa_mesh = resp_json["collection"][0]["@id"]

            page_py = wiki_wiki.page(name)
            sa_wiki=""
            if page_py.exists():
                sa_wiki = page_py.fullurl
            
            row.update({"NCBITAXON": sa_ncbi,
                        "MESH": sa_mesh,
                        "Wikipedia": sa_wiki})
            csv_writer.writerow(row)
