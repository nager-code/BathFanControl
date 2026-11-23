import json,collections,sys
d=json.load(open(sys.argv[1])); skip=set(sys.argv[2:])
c=collections.Counter(v["type"] for v in d["violations"]); print(dict(c), "unverbunden:", len(d.get("unconnected_items",[])), "Schaltplanabgleich:", len(d.get("schematic_parity",[])))
for v in d.get("unconnected_items",[])+d.get("schematic_parity",[]):
    print("  >>",v["description"][:60],"|",[ (i["description"][:50], round(i["pos"]["x"]-100,2), round(i["pos"]["y"]-100,2)) for i in v["items"]][:2])
for v in d["violations"]:
    if v["type"] in skip: continue
    print(v["type"],"|",v["description"][:120],"|",[ (i["description"][:45], round(i["pos"]["x"]-100,2), round(i["pos"]["y"]-100,2)) for i in v["items"]][:2])
