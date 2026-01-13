
from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        inizio = self._view.dp1.value
        fine = self._view.dp2.value
        categoria = self._view.dd_category.value
        self._model.build_graph(inizio,fine,categoria)
        self._view.txt_risultato.clean()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start Date: {inizio}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End Date: {fine}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {len(self._model.G.nodes())}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {len(self._model.G.edges())}"))
        self._view.update()

        #popolo i dropdown prodotti
        for n in self._model.G.nodes():
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(text = n.product_name))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(text=n.product_name))
        self._view.update()


    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        # corrispondono ai migliori 5 per vendite
        best_prodotti = []
        for n in self._model.G.nodes:
            score = 0
            for n_out in self._model.G.successors(n):
                score += self._model.G[n][n_out]["weight"]
            for n_in in self._model.G.predecessors(n):
                score -= self._model.G[n_in][n]["weight"]

            best_prodotti.append((n, score))

        best_prodotti.sort(reverse=True, key=lambda x: x[1])
        self._view.txt_risultato.controls.append(ft.Text(f"\nI cinque prodotti più venduti sono:"))
        for p in best_prodotti[0:5]:
            self._view.txt_risultato.controls.append(ft.Text(f"{p[0].product_name} with score {p[1]}"))
        self._view.update()





    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        p = self._view.dd_prodotto_iniziale.value
        a = self._view.dd_prodotto_finale.value
        lunghezza = int(self._view.txt_lunghezza_cammino.value)
        self._model.best_cammino(lunghezza,p,a)
        if len(self._model.best_path) == 0:
            self._view.show_alert("Nessun cammino trovato con i dati di inizio e fine richiesti")
        else:
            self._view.txt_risultato.clean()
            self._view.txt_risultato.controls.append(ft.Text("Cammino migliore:"))
            for a in self._model.best_path:
                self._view.txt_risultato.controls.append(ft.Text(f"{a}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Score: {self._model.best_peso}"))
            self._view.update()

    def handle_popola_dd(self):
        self._model.trova_categorie()
        for c in self._model.categorie:
            self._view.dd_category.options.append(ft.dropdown.Option(text = str(c)))
        self._view.update()

