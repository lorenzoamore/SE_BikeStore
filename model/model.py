import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.categorie = []
        self.G = nx.DiGraph()
        self.nodi = []
        self.best_path = []
        self.best_peso = -1


    def get_date_range(self):
        return DAO.get_date_range()

    def trova_categorie(self):
        self.categorie = DAO.get_categories()


    def build_graph(self,inizio,fine,categoria):
        self.G.clear()
        self.nodi = DAO.get_product(categoria)
        self.G.add_nodes_from(self.nodi)

        prodotti_vendite= DAO.get_prodotti_venduti(inizio,fine,categoria)
        for n in self.nodi:
            for v in prodotti_vendite:
                if n == v:
                    n.vendite = v.vendite
                if v not in self.nodi:
                    self.G.add_node(v)

        for p in self.G.nodes():
            for d in prodotti_vendite:
                if p == d:
                    continue
                else:
                    if p.vendite >= d.vendite:
                        self.G.add_edge(p,d,weight = p.vendite + d.vendite)

    def best_cammino(self,lunghezza,p,a):
        self.best_path = []
        self.best_peso = -1

        partenza = ""
        arrivo = ""
        for n in self.G.nodes():
            if n.product_name == p:
                partenza = n
            if n.product_name == a:
                arrivo = n
        self._ricorsione(lunghezza, 0, [partenza], arrivo)


    def _ricorsione(self, lunghezza, peso, path, arrivo):
        if len(path) == lunghezza:
            print(f"Raggiunta lunghezza {lunghezza}. Ultimo nodo: {path[-1]}, Target: {arrivo}")
            if path[-1] == arrivo:
                print(f"TROVATOOOOOO")
                if peso > self.best_peso:
                    self.best_peso = peso
                    self.best_path = path.copy()
            return

        for v in list(self.G.successors(path[-1])):
            if v not in path:
                p = self.G[path[-1]][v]["weight"]
                path.append(v)
                self._ricorsione(lunghezza,
                                 peso + p,
                                 path,
                                 arrivo)
                path.pop()






