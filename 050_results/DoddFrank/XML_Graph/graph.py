import lxml.etree as etree
import networkx as nx
import matplotlib.pyplot as plt

# parse XML
events = ("start", "end")
context = etree.iterparse('DFA.xml', events=events)

#extract titles
titles = []
for action, elem in context:
    #print action, ':', elem.tag
    if action == "start":
        if elem.tag == "title":
            titles.append(elem)


structure = ['title', 'subtitle', 'part', 'section', 'subsection', 'paragraph', 'subparagraph', 'clause', 'subclause', 'item', 'subitem']

def graph(elem, G):
    if (list(elem)) and (elem.tag in structure):
        for el in list(elem):
            if el.tag in structure:
                G.add_node(el)
                edge = (elem, el)
                G.add_edge(*edge)
                graph(el, G)
            elif el.tag == 'continuation-text':
                G.add_node(el)
                for e in list(elem):
                    if e.tag in structure:
                        edge = (e, el)
                        G.add_edge(*edge)
                graph(el, G)
            elif el.tag == 'quoted-block':
                for e in list(el):
                    if e.tag in structure:
                        G.add_node(e)
                        edge = (elem, e)
                        G.add_edge(*edge)
                graph(el, G)

# one single graph
G = nx.Graph()
for elem in titles:
    if elem.tag in structure:
        G.add_node(elem)
        graph(elem, G)

nx.write_gexf(G, 'allTitles.gexf')

# one graph per title
c = 1
for elem in titles:
    H = nx.Graph()
    if elem.tag in structure:
        H.add_node(elem)
        graph(elem, H)
    nx.write_gexf(H, 'title_%s.gexf' %c)
    c = c+1



#print(G.nodes())
#print(G.edges())

#nx.draw(G, with_labels=True)
#plt.savefig("try.png") # save as png
#plt.show() # display
