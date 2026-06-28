import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.id_attori = {}
        self._percorso_ottimo = []


    def get_rates(self):
        return DAO.get_rates()

    def crea_grafo(self, minimo, massimo):
        self._grafo.clear()
        self.id_attori = {}

        nodi = DAO.get_nodi(minimo, massimo)
        for n in nodi:
            self.id_attori[n.id] = n

        self._grafo.add_nodes_from(nodi)
        self._grafo.add_weighted_edges_from(DAO.get_archi(self.id_attori, minimo, massimo))

    def dim_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_maggiori(self):
        archi = [(a,b,self._grafo[a][b]["weight"]) for a,b in self._grafo.edges]
        archi.sort(key=lambda x:x[2], reverse=True)

        if len(archi) > 5:
            return archi[:5]
        else:
            return archi

    def get_connesse(self):
        componenti = list(nx.connected_components(self._grafo))
        componenti.sort(key=lambda x:len(x), reverse=True)

        return len(componenti), componenti[0] if len(componenti) else []

    def get_percorso(self):
        self._percorso_ottimo = []

        for n in self._grafo.nodes:
            self._ricorsione([n])

        return self._percorso_ottimo

    def _ricorsione(self, parziale):
        if len(parziale) > len(self._percorso_ottimo):
            self._percorso_ottimo = copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            #if n not in parziale:             # NODI NON RIPETUTI
                if n.get_age() < parziale[-1].get_age():
                    parziale.append(n)
                    if self.is_semplice(parziale):              # ARCHI NON RIPETUTI
                        self._ricorsione(parziale)
                    parziale.pop()


    def is_semplice(self, parziale):
        if len(parziale) < 3:
            return True

        ultimo = (parziale[-2], parziale[-1])
        archi = [(parziale[i], parziale[i + 1]) for i in range(len(parziale) - 2)]

        return ultimo not in archi
