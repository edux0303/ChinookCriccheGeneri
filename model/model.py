import networkx as nx
from itertools import combinations
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._nomiClienti = {}
        # punto 2
        self._N = 0
        self._grupBest = []
        self._pesoBest = -1
        self._ricavoBest = -1
        self._candidati = []

    # ==================== PUNTO 1 ====================

    def getPaesi(self):
        return DAO.getCountry()

    def buildGraph(self, paese, soglia):
        self._grafo.clear()
        self._idMap = {}

        # nodi: generi acquistati da clienti del paese
        nodi = DAO.getNodi(paese)
        self._idMap = {g.id: g for g in nodi}
        self._grafo.add_nodes_from(nodi)

        # set dei clienti di ogni genere
        for idG, idC in DAO.getCoppia(paese):
            if idG in self._idMap:
                self._idMap[idG].clienti.add(idC)

        # archi: almeno 'soglia' clienti in comune
        for g1, g2 in combinations(nodi, 2):
            comuni = g1.clienti & g2.clienti
            if len(comuni) >= soglia:
                self._grafo.add_edge(g1, g2, weight=len(comuni))

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda g: g.name)

    def getGenere(self, idG):
        return self._idMap.get(idG)

    # a) genere con ricavo maggiore
    def getRicavoMaggiore(self):
        best = max(self._grafo.nodes, key=lambda g: g.ricavo)
        return best, best.ricavo

    # b) genere con più brani venduti
    def getPiuBrani(self):
        best = max(self._grafo.nodes, key=lambda g: g.numeroBrani)
        return best, best.numeroBrani

    # c) generi con più clienti (anche a pari merito)
    def getPiuClienti(self):
        maxClienti = max(len(g.clienti) for g in self._grafo.nodes)
        migliori = [g for g in self._grafo.nodes if len(g.clienti) == maxClienti]
        migliori.sort(key=lambda g: g.name)
        return migliori, maxClienti

    # d) generi con grado maggiore (anche a pari merito)
    def getGradoMaggiore(self):
        maxGrado = max(self._grafo.degree(g) for g in self._grafo.nodes)
        migliori = [g for g in self._grafo.nodes if self._grafo.degree(g) == maxGrado]
        migliori.sort(key=lambda g: g.name)
        return migliori, maxGrado

    # e) 5 archi di peso maggiore
    def getTop5Archi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([u.name, v.name])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]

    # f) componenti connesse
    def getInfoComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        isolati = 0
        for comp in componenti:
            if len(comp) == 1:
                isolati += 1
        return len(componenti), len(piuGrande), isolati

    # g) numero di clienti e clienti con più generi diversi
    def getClientePiuGeneri(self):
        conta = {}                                   # {CustomerId: numero di generi}
        for g in self._grafo.nodes:
            for c in g.clienti:
                conta[c] = conta.get(c, 0) + 1
        maxGeneri = max(conta.values())
        if len(self._nomiClienti) == 0:
            self._nomiClienti = DAO.getClienti()     # {CustomerId: "Nome Cognome"}
        migliori = [self._nomiClienti[c] for c in conta if conta[c] == maxGeneri]
        migliori.sort()
        return len(conta), migliori, maxGeneri

    # h) generi di nicchia (un solo cliente)
    def getNicchia(self):
        nicchia = [g for g in self._grafo.nodes if len(g.clienti) == 1]
        nicchia.sort(key=lambda g: g.name)
        return nicchia

    # ==================== PUNTO 2 ====================

    def getCricca(self, partenza, N):
        self._N = N
        self._grupBest = []
        self._pesoBest = -1
        self._ricavoBest = -1
        # candidati: solo i vicini della partenza
        self._candidati = sorted(self._grafo.neighbors(partenza), key=lambda g: g.name)
        self._ricorsione([partenza], 0, 0)
        return self._grupBest, self._pesoBest, self._ricavoBest

    def _ricorsione(self, parziale, start, pesoParziale):
        # caso terminale: ho N generi
        if len(parziale) == self._N:
            ricavo = sum(g.ricavo for g in parziale)
            if (pesoParziale > self._pesoBest or
                    (pesoParziale == self._pesoBest and ricavo > self._ricavoBest)):
                self._pesoBest = pesoParziale
                self._ricavoBest = ricavo
                self._grupBest = list(parziale)
            return

        for j in range(start, len(self._candidati)):
            candidato = self._candidati[j]

            # vincolo cricca: collegato a TUTTI quelli già nel gruppo
            collegato = True
            for p in parziale:
                if not self._grafo.has_edge(candidato, p):
                    collegato = False
                    break
            if not collegato:
                continue

            # peso aggiunto: archi del candidato con tutti quelli già nel gruppo
            pesoNuovo = 0
            for p in parziale:
                pesoNuovo += self._grafo[candidato][p]["weight"]

            parziale.append(candidato)
            self._ricorsione(parziale, j + 1, pesoParziale + pesoNuovo)
            parziale.pop()