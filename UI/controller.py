import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        for r in self._model.get_rates():
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        minimo = self._view._ddrating1.value
        massimo = self._view._ddrating2.value


        if minimo is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un minimo", color="red"))
            self._view.update_page()
            return

        if massimo is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un massimo", color="red"))
            self._view.update_page()
            return

        try:
            minimo = float(minimo)
            massimo = float(massimo)
        except:
            self._view.txt_result.controls.append(ft.Text("Selezionare valori validi", color="red"))
            self._view.update_page()
            return

        if minimo > massimo:
            self._view.txt_result.controls.append(ft.Text("Minimo deve essere inferiore a massimo", color="red"))
            self._view.update_page()
            return


        self._model.crea_grafo(minimo, massimo)

        n, m = self._model.dim_grafo()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi:", color="green"))
        for a,b,w in self._model.get_maggiori():
            self._view.txt_result.controls.append(ft.Text(f"{a} -> {b} : {w}"))

        lun, comp = self._model.get_connesse()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {lun} componenti connesse", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(comp)}:", color="green"))

        for n in comp:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))

        self._view._btnCammino.disabled = False
        self._view.update_page()

    def handleCammino(self, e):
        percorso = self._model.get_percorso()
        self._view.txt_result.controls.append(
            ft.Text(f"Il percorso più lungo è {len(percorso)}:", color="green"))

        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{n} ({n.get_age()})"))

        self._view.update_page()
