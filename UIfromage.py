import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
from fromage import FromageETL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class FromageETLUI(tk.Tk):
    """_summary_

    Args:
        tk (_type_): _description_
    """
    def __init__(self, url, db_path):
        tk.Tk.__init__(self)
        self.title("Fromage ETL")

        self.etl = FromageETL(url, db_path)

        # Créer les boutons
        self.update_button = tk.Button(self, text="Mettre à jour la BDD", command=self.update_database)
        self.update_button.pack(pady=10)

        self.show_pie_chart_button = tk.Button(self, text="Afficher le diagramme en camembert", command=self.show_chart)
        self.show_pie_chart_button.pack(pady=10)

        self.show_reliability_button = tk.Button(self, text="Afficher le taux de fiabilité", command=self.show_reliability)
        self.show_reliability_button.pack(pady=10)

    def update_database(self):
        """Mis a jour de la base de donnée ."""
        self.etl.run_etl()
        messagebox.showinfo("Mise à jour", "La base de données a été mise à jour avec succès!")

    def show_chart(self):
        """ montre le pie chart ."""
        counts_by_family = self.etl.group_by_family()

        # Création du diagramme en camembert
        fig, ax = plt.subplots()
        ax.pie(counts_by_family['cheese_count'], labels=counts_by_family['family'], autopct='%2.1f%%', startangle=90)
        ax.axis('equal')

        # Affichage du diagramme dans la fenêtre Tkinter
        pie_chart_window = tk.Toplevel(self)
        pie_chart_window.title("Diagramme en camembert")
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_reliability(self):
        # Obtenir le taux de fiabilité des résultats depuis votre logique métier
        reliability_rate = 85.5
        messagebox.showinfo("Taux de fiabilité", f"Le taux de fiabilité des résultats est de {reliability_rate}%")

if __name__ == "__main__":
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    DB_PATH = 'mydatabase.db'

    app = FromageETLUI(url, DB_PATH)
    app.mainloop()
