import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.categorie = []
        self.G = nx.DiGraph()
        self.nodi = []


    def get_date_range(self):
        return DAO.get_date_range()

    def trova_categorie(self):
        self.categorie = DAO.get_categories()


    def build_graph(self,inizio,fine,categoria):
        self.G.clear()
        self.nodi = DAO.get_product(categoria)
        self.G.add_nodes_from(self.nodi)

        prodotti_vendite= DAO.get_prodotti_venduti(inizio,fine,categoria)
        maggiori = []
        for p in prodotti_vendite:
            for d in prodotti_vendite:
                if p == d:
                    continue
                else:
                    if p.vendite >= d.vendite:
                        self.G.add_edge(p,d,weight = p.vendite + d.vendite)








