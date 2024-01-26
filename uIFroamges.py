import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fromage import FromageETL

class FromageETLUI(tk.Tk):
    def __init__(self, url, db_path):
        tk.Tk.__init__(self)
        self.title("Fromage ETL")

        self.etl = FromageETL(url, db_path)

        # Créer les boutons
        self.update_button = tk.Button(self, text="Mettre à jour la BDD", command=self.update_database)
        self.update_button.pack(pady=10)

        self.show_pie_chart_button = tk.Button(self, text="Afficher le diagramme en camembert", command=self.show_pie_chart)
        self.show_pie_chart_button.pack(pady=10)

        self.show_reliability_button = tk.Button(self, text="Afficher le taux de fiabilité", command=self.show_reliability)
        self.show_reliability_button.pack(pady=10)

    def update_database(self):
        self.etl.run_etl()
        messagebox.showinfo("Mise à jour", "La base de données a été mise à jour avec succès!")

    def show_pie_chart(self):
        counts_by_family = self.etl.group_by_family()

        # Création du diagramme en camembert
        fig, ax = plt.subplots(figsize=(25, 50))
        ax.pie(counts_by_family['cheese_count'], labels=counts_by_family['family'], autopct='%1.2f%%', startangle=90,counterclock=False)
        ax.axis('equal')

        # Ajout de la légende
        plt.legend(counts_by_family['family'], title='Familles', loc='center left', bbox_to_anchor=(1, 0.5))

        # Affichage du diagramme dans la fenêtre Tkinter
        pie_chart_window = tk.Toplevel(self)
        pie_chart_window.title("Diagramme en camembert")
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_reliability(self):
        # Ajoutez votre logique pour calculer le taux de fiabilité ici
        reliability_rate = 85.5
        messagebox.showinfo("Taux de fiabilité", f"Le taux de fiabilité des résultats est de {reliability_rate}%")

if __name__ == "__main__":
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    db_path = 'fromage_database.db'

    app = FromageETLUI(url, db_path)
    app.mainloop()
