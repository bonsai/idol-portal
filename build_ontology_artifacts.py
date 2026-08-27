import rdflib, sqlite3, json, html, os

BASE = os.path.dirname(os.path.abspath(__file__))
TTL = os.path.join(BASE, "ontology.ttl")
NS = "https://idol-folklore.example/ns#"

g = rdflib.Graph()
g.parse(TTL, format="turtle")

# ---------- 1) SQLite ----------
con = sqlite3.connect(os.path.join(BASE, "ontology.sqlite"))
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS triples")
cur.execute("""CREATE TABLE triples (
    id INTEGER PRIMARY KEY,
    subject TEXT,
    predicate TEXT,
    object TEXT,
    lang TEXT,
    datatype TEXT
)""")
def localname(uri):
    s = str(uri)
    for pre in ("http://www.w3.org/1999/02/22-rdf-syntax-ns#",
               "http://www.w3.org/2000/01/rdf-schema#",
               "http://www.w3.org/2002/07/owl#",
               "http://www.w3.org/2004/02/skos/core#",
               NS):
        if s.startswith(pre):
            return s[len(pre):]
    return s

rows = []
for s, p, o in g:
    lang = o.language if isinstance(o, rdflib.Literal) else None
    dt = str(o.datatype) if isinstance(o, rdflib.Literal) and o.datatype else None
    obj = str(o)
    rows.append((str(s), str(p), obj, lang, dt))
cur.executemany("INSERT INTO triples(subject,predicate,object,lang,datatype) VALUES (?,?,?,?,?)", rows)
cur.execute("CREATE INDEX IF NOT EXISTS idx_subject ON triples(subject)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_predicate ON triples(predicate)")
con.commit()
con.close()
print("sqlite triples:", len(rows))

# ---------- 2) Graph (nodes / edges) ----------
nodes = {}
edges = []
REL_LABELS = {
    "http://www.w3.org/2000/01/rdf-schema#subClassOf": "subClassOf",
    "http://www.w3.org/2004/02/skos/core#broader": "broader",
    "https://idol-folklore.example/ns#類似する": "類似する",
    "https://idol-folklore.example/ns#可視化する": "可視化する",
    "https://idol-folklore.example/ns#構成する": "構成する",
    "https://idol-folklore.example/ns#拡張する": "拡張する",
    "https://idol-folklore.example/ns#参加する": "参加する",
    "https://idol-folklore.example/ns#変容する": "変容する",
}

def add_node(uri, group):
    n = localname(uri)
    if n not in nodes:
        nodes[n] = {"id": n, "label": n, "group": group}

for s, p, o in g:
    ps = str(p)
    if ps in REL_LABELS:
        if isinstance(o, rdflib.URIRef):
            add_node(s, "rel")
            add_node(o, "rel")
            edges.append({"from": localname(s), "to": localname(o), "label": REL_LABELS[ps]})

# node type from rdf:type
TYPE_GROUP = {
    "http://www.w3.org/2002/07/owl#Class": "Class",
    "http://www.w3.org/2004/02/skos/core#Concept": "Concept",
    "http://www.w3.org/2002/07/owl#ObjectProperty": "Property",
    "http://www.w3.org/2004/02/skos/core#ConceptScheme": "Scheme",
}
for s, p, o in g:
    if str(p) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and isinstance(o, rdflib.URIRef):
        grp = TYPE_GROUP.get(str(o))
        if grp and localname(s) in nodes:
            nodes[localname(s)]["group"] = grp

# labels from rdfs:label / skos:prefLabel
for s, p, o in g:
    if str(p) in ("http://www.w3.org/2000/01/rdf-schema#label",
                  "http://www.w3.org/2004/02/skos/core#prefLabel") and isinstance(o, rdflib.Literal):
        n = localname(s)
        if n in nodes:
            nodes[n]["label"] = str(o)

graph = {"nodes": list(nodes.values()), "edges": edges}
with open(os.path.join(BASE, "ontology.graph.json"), "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
print("nodes:", len(nodes), "edges:", len(edges))

# ---------- 3) HTML (vis-network) ----------
data_json = html.escape(json.dumps(graph, ensure_ascii=False))
html_doc = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>アイドル民俗学オントロジー グラフ</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>body{{margin:0;font-family:system-ui,"Yu Gothic",sans-serif;background:#fff0f6}}
#title{{padding:14px 18px;color:#e23c80;font-weight:800}}
#net{{height:82vh;width:100%}}</style></head>
<body><div id="title">アイドル民俗学オントロジー グラフ（vis-network）</div>
<div id="net"></div>
<script>
const graph = {data_json};
const groups = {{Class:"#ff5b9b",Concept:"#b3e5fc",Property:"#c8e6c9",Scheme:"#d1c4e9",rel:"#ffccbc"}};
const nodes = new vis.DataSet(graph.nodes.map(n=>({{id:n.id,label:n.label,group:n.group}})));
const edges = new vis.DataSet(graph.edges.map(e=>({{from:e.from,to:e.to,label:e.label,arrows:"to",font:{{size:11}},smooth:true}})));
new vis.Network(document.getElementById("net"),{{nodes,edges}},{{
  groups, layout:{{hierarchical:false}}, physics:{{barnesHut:{{gravitationalConstant:-8000}}}},
  edges:{{arrows:{{to:{{scaleFactor:0.5}}}}}}, interaction:{{hover:true}}
}});
</script></body></html>"""
with open(os.path.join(BASE, "ontology.graph.html"), "w", encoding="utf-8") as f:
    f.write(html_doc)

# ---------- 4) DOT ----------
GROUPS = {"Class":"#ff5b9b","Concept":"#b3e5fc","Property":"#c8e6c9","Scheme":"#d1c4e9","rel":"#ffccbc"}
lines = ["digraph idol_folklore {", '  rankdir="TB";', '  node [shape=box,style="rounded,filled",fillcolor="#fff0f6",color="#e23c80"];']
for n in nodes.values():
    lines.append(f'  "{n["id"]}" [label="{n["label"]}",fillcolor="{GROUPS.get(n["group"],"#fff0f6")}"];')
for e in edges:
    lines.append(f'  "{e["from"]}" -> "{e["to"]}" [label="{e["label"]}"];')
lines.append("}")
with open(os.path.join(BASE, "ontology.dot"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("done")
