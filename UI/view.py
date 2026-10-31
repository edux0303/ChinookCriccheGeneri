import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - ChinookCriccheGeneri"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - ChinookCriccheGeneri", color="blue", size=24)
        self._page.controls.append(self._title)

        # ---------- PUNTO 1 ----------
        self._ddCountry = ft.Dropdown(label="Paese")
        self._txtInS = ft.TextField(label="Soglia clienti S")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo)

        row1 = ft.Row([ft.Container(self._ddCountry, width=250),
                       ft.Container(self._txtInS, width=150),
                       ft.Container(self._btnCreaGrafo, width=150),
                       ft.Container(self._btnStampaInfo, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # ---------- PUNTO 2 ----------
        self._ddGenere = ft.Dropdown(label="Genere di partenza")
        self._txtInN = ft.TextField(label="N (generi nel gruppo)")
        self._btnCricca = ft.ElevatedButton(text="Trova pacchetto",
                                            on_click=self._controller.handleCricca)

        row2 = ft.Row([ft.Container(self._ddGenere, width=250),
                       ft.Container(self._txtInN, width=150),
                       ft.Container(self._btnCricca, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)

        # riempio i paesi all'avvio
        self._controller.fillDDPaesi()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()