from database.DB_connect import DBConnect
from model.genere import Genere
"""
1. All’avvio, riempire un menu a tendina con tutti i paesi dei clienti (Customer.Country), in ordine alfabetico.
2. L’utente sceglie un paese P e inserisce un intero S ≥ 1. Premendo “Crea Grafo”, l’applicazione costruisce un grafo semplice, non orientato e pesato: a) i nodi sono i generi acquistati da almeno un cliente del paese P. Per ogni genere si memorizzino, considerando solo i clienti del paese P:
    * il ricavo totale;
    * il numero di brani venduti;
    * l’insieme dei clienti che lo hanno acquistato; b) due generi sono collegati da un arco se hanno almeno S clienti in comune; c) il peso dell’arco è il numero di clienti in comune.
3. Stampare il numero di nodi e di archi. Riempire poi un menu a tendina con i generi del grafo, in ordine alfabetico.
4. Premendo “Stampa Info”, stampare: a) il genere con il ricavo maggiore e il ricavo; b) il genere con più brani venduti e il numero; c) il genere (o i generi, se a pari merito) con più clienti e il numero; d) il genere (o i generi) con grado maggiore e il grado; e) i 5 archi di peso maggiore, in ordine decrescente di peso. A parità si ordina alfabeticamente per il primo genere e poi per il secondo; f) il numero di componenti connesse, la dimensione della più grande e il numero di generi isolati; g) il numero di clienti del paese presenti nel grafo e il cliente (o i clienti) che ha acquistato più generi diversi, con nome, cognome e numero di generi; h) i generi di nicchia, cioè acquistati da un solo cliente del paese: quanti sono e l’elenco in ordine alfabetico.
PUNTO 2
Si vuole costruire un pacchetto di generi da proporre ai clienti del paese. L’utente sceglie un genere di partenza G e inserisce un intero N ≥ 2. Con un algoritmo ricorsivo, trovare un gruppo di esattamente N generi che:
1. contiene il genere G;
2. è una cricca: ogni coppia di generi del gruppo è collegata da un arco del grafo;
3. massimizza la somma dei pesi di tutti gli archi interni al gruppo;
4. a parità di peso, ha il ricavo totale maggiore




"""
class DAO():
    @staticmethod
    def getCountry():
        """Paesi dei clienti, in ordine alfabetico."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT c.Country AS paese
                FROM Customer c
                ORDER BY c.Country
                """
        cursor.execute(query)
        for row in cursor:
            results.append(row["paese"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(paese):
        conn = DBConnect.get_connection()
        if conn is None:
            return []

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT g.GenreId AS id, g.Name AS nome,
                       SUM(il.Quantity * il.UnitPrice) AS ricavo, SUM(il.Quantity) AS numero
                FROM Genre g, Track t, InvoiceLine il, Invoice i, Customer c
                WHERE g.GenreId = t.GenreId AND t.TrackId = il.TrackId AND i.InvoiceId = il.InvoiceId
                AND c.CustomerId = i.CustomerId AND c.Country = %s
                GROUP BY g.GenreId, g.Name
                ORDER BY g.GenreId
                """
        cursor.execute(query, (paese,))

        for row in cursor:
            results.append(Genere(row["id"], row["nome"], float(row["ricavo"]), int(row["numero"])))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppia(paese):
        conn = DBConnect.get_connection()
        if conn is None:
            return []

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT t.GenreId AS idG, i.CustomerId AS idC
                FROM Track t, InvoiceLine il, Invoice i, Customer c
                WHERE t.TrackId = il.TrackId AND i.InvoiceId = il.InvoiceId
                AND c.CustomerId = i.CustomerId AND c.Country = %s
                ORDER BY t.GenreId
                """
        cursor.execute(query, (paese,))

        for row in cursor:
            results.append((row["idG"], row["idC"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getClienti():
        conn = DBConnect.get_connection()
        if conn is None:
            return {}

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT c.CustomerId, c.FirstName, c.LastName
                FROM Customer c
                """
        cursor.execute(query)

        for row in cursor:
            results[row["CustomerId"]] = f"{row['FirstName']} {row['LastName']}"

        cursor.close()
        conn.close()
        return results
