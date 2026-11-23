import re,sys
def parse(path):
    t=open(path).read()
    nets={}
    for m in re.finditer(r'\(net\s+\(code\s+"?\d+"?\)\s+\(name\s+"([^"]*)"\)(.*?)\n\s*\)(?=\s*\(net|\s*\)\s*\)?\s*$)',t,re.S):
        name=m.group(1).lstrip('/')
        nodes=set(re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)',m.group(2)))
        nets[name]=nodes
    return nets
if __name__=="__main__":
    a=parse(sys.argv[1]); b=parse(sys.argv[2])
    print(len(a),len(b))
    for n in sorted(set(a)|set(b)):
        if a.get(n)!=b.get(n): print("DIFF",n,sorted(a.get(n,[])),"|",sorted(b.get(n,[])))
    print("compare done")
