import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # ---------- PUNTO 1 ----------

    def fillDDPaesi(self):
        self._view._ddCountry.options.clear()
        for p in self._model.getPaesi():
            self._view._ddCountry.options.append(ft.dropdown.Option(key=p, text=p))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        # 1. paese
        if self._view._ddCountry.value is None:
            self._errore("Seleziona un paese!")
            return
        paese = self._view._ddCountry.value

        # 2. soglia S
        try:
            soglia = int(self._view._txtInS.value)
        except (ValueError, TypeError):
            self._errore("S deve essere un numero intero!")
            return
        if soglia < 1:
            self._errore("S deve essere almeno 1!")
            return

        # 3. grafo
        self._model.buildGraph(paese, soglia)

        if self._model.getNumNodi() == 0:
            self._errore("Nessun genere acquistato dai clienti di questo paese.")
            return

        # 4. stampo
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # 5. dropdown generi
        self.fillDDGeneri()

        self._view.update_page()

    def fillDDGeneri(self):
        self._view._ddGenere.options.clear()
        self._view._ddGenere.value = None
        for g in self._model.getNodiOrdinati():
            self._view._ddGenere.options.append(ft.dropdown.Option(key=str(g.id), text=g.name))

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        res = self._view._txt_result.controls

        # a) ricavo maggiore
        genere, ricavo = self._model.getRicavoMaggiore()
        res.append(ft.Text(f"a) Genere con ricavo maggiore: {genere} ({ricavo:.2f} $)"))

        # b) più brani venduti
        genere, brani = self._model.getPiuBrani()
        res.append(ft.Text(f"b) Genere con più brani venduti: {genere} ({brani} brani)"))

        # c) più clienti
        lista, n = self._model.getPiuClienti()
        res.append(ft.Text(f"c) Genere con più clienti ({n}): {', '.join(str(g) for g in lista)}"))

        # d) grado maggiore
        lista, grado = self._model.getGradoMaggiore()
        res.append(ft.Text(f"d) Genere con grado maggiore ({grado}): {', '.join(str(g) for g in lista)}"))

        # e) top 5 archi
        res.append(ft.Text("e) I 5 archi di peso maggiore:"))
        for n1, n2, peso in self._model.getTop5Archi():
            res.append(ft.Text(f"     {n1} – {n2}: {peso}"))

        # f) componenti
        nComp, dimMax, isolati = self._model.getInfoComponenti()
        res.append(ft.Text(f"f) Componenti connesse: {nComp}"))
        res.append(ft.Text(f"     Dimensione della più grande: {dimMax}"))
        res.append(ft.Text(f"     Generi isolati: {isolati}"))

        # g) clienti e cliente con più generi
        nClienti, lista, nGeneri = self._model.getClientePiuGeneri()
        res.append(ft.Text(f"g) Clienti del paese nel grafo: {nClienti}"))
        res.append(ft.Text(f"     Cliente con più generi diversi ({nGeneri}): {', '.join(lista)}"))

        # h) generi di nicchia
        nicchia = self._model.getNicchia()
        res.append(ft.Text(f"h) Generi di nicchia (un solo cliente): {len(nicchia)}"))
        for g in nicchia:
            res.append(ft.Text(f"     {g}"))

        self._view.update_page()

    # ---------- PUNTO 2 ----------

    def handleCricca(self, e):
        self._view._txt_result.controls.clear()

        # 1. grafo creato?
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        # 2. genere di partenza
        if self._view._ddGenere.value is None:
            self._errore("Seleziona un genere di partenza!")
            return
        partenza = self._model.getGenere(int(self._view._ddGenere.value))
        if partenza is None:
            self._errore("Genere non presente nel grafo!")
            return

        # 3. N
        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un numero intero!")
            return
        if N < 2:
            self._errore("N deve essere almeno 2!")
            return
        if N > self._model.getNumNodi():
            self._errore(f"N non può superare il numero di generi ({self._model.getNumNodi()})!")
            return

        # 4. ricorsione
        gruppo, peso, ricavo = self._model.getCricca(partenza, N)

        if len(gruppo) == 0:
            self._errore(f"Nessuna cricca di {N} generi contenente {partenza}.")
            return

        # 5. stampo
        res = self._view._txt_result.controls
        res.append(ft.Text(f"Pacchetto di {N} generi con {partenza}:", color="green"))
        for g in sorted(gruppo, key=lambda x: x.name):
            res.append(ft.Text(f"     {g} – ricavo {g.ricavo:.2f} $"))
        res.append(ft.Text(f"Peso totale degli archi interni: {peso}"))
        res.append(ft.Text(f"Ricavo totale: {ricavo:.2f} $"))

        self._view.update_page()

    # ---------- UTILITY ----------

    def _errore(self, messaggio):
        self._view._txt_result.controls.append(ft.Text(messaggio, color="red"))
        self._view.update_page()