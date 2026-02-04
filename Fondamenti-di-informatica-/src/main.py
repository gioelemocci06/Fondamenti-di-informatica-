"""
========================================================
SISTEMA DI GESTIONE DELLE SPESE PERSONALI E DEL BUDGET
========================================================
Progetto Finale - Fondamenti di Informatica
Studente: gioelemocci06
Repository: https://github.com/gioelemocci06/Fondamenti-di-informatica-

Descrizione:
Sistema console-based per la gestione delle spese personali
con database SQLite relazionale.

Funzionalità:
1. Gestione Categorie
2. Inserimento Spese
3. Definizione Budget Mensile
4. Visualizzazione Report (3 tipi)
========================================================
"""

import sqlite3
from datetime import datetime
import os


class SistemaSpese:
    """
    Classe principale per la gestione del sistema spese
    """
    
    def __init__(self, db_name="spese_personali.db"):
        """
        Inizializza il sistema e crea il database
        
        Args:
            db_name (str): Nome del file database SQLite
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connetti_database()
        self.crea_tabelle()
    
    def connetti_database(self):
        """
        Connette al database SQLite
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ Connessione al database '{self.db_name}' riuscita.")
        except sqlite3.Error as e:
            print(f"✗ Errore nella connessione al database: {e}")
            exit(1)
    
    def crea_tabelle(self):
        """
        Crea le tabelle necessarie se non esistono
        Con tutti i vincoli di integrità richiesti:
        - PRIMARY KEY
        - FOREIGN KEY
        - CHECK
        - UNIQUE
        - NOT NULL
        """
        try:
            # ==========================================
            # TABELLA CATEGORIE
            # ==========================================
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL
                )
            ''')
            
            # ==========================================
            # TABELLA SPESE
            # ==========================================
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS spese (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    importo REAL NOT NULL CHECK(importo > 0),
                    categoria_id INTEGER NOT NULL,
                    descrizione TEXT,
                    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                )
            ''')
            
            # ==========================================
            # TABELLA BUDGET
            # ==========================================
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS budget (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mese TEXT NOT NULL,
                    categoria_id INTEGER NOT NULL,
                    importo REAL NOT NULL CHECK(importo > 0),
                    UNIQUE(mese, categoria_id),
                    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                )
            ''')
            
            self.conn.commit()
            print("✓ Tabelle del database create/verificate correttamente.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nella creazione delle tabelle: {e}")
    
    def chiudi_connessione(self):
        """
        Chiude la connessione al database
        """
        if self.conn:
            self.conn.close()
            print("\n✓ Connessione al database chiusa.")
    
    def pulisci_schermo(self):
        """
        Pulisce lo schermo della console
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausa(self):
        """
        Mette in pausa il programma
        """
        input("\nPremi INVIO per continuare...")
    
    # ========================================
    # MODULO 1: GESTIONE CATEGORIE
    # ========================================
    
    def gestione_categorie(self):
        """
        MODULO 1 - Gestione delle Categorie
        
        Obiettivo: Consentire all'utente di definire le categorie di spesa
        
        Input: Nome della categoria (stringa)
        Elaborazione:
        1. Lettura del nome della categoria
        2. Verifica che il nome non sia vuoto
        3. Controllo dell'esistenza della categoria (SQL SELECT)
        4. Inserimento della categoria se valida (SQL INSERT)
        Output: Messaggio di successo o errore
        """
        print("\n" + "="*50)
        print("GESTIONE CATEGORIE")
        print("="*50)
        
        # INPUT
        nome_categoria = input("\nInserisci il nome della categoria: ").strip()
        
        # ELABORAZIONE
        
        # Step 1 e 2: Verifica che il nome non sia vuoto
        if not nome_categoria:
            print("✗ Errore: il nome della categoria non può essere vuoto.")
            self.pausa()
            return
        
        try:
            # Step 3: Controllo dell'esistenza della categoria (SQL SELECT)
            self.cursor.execute(
                "SELECT id FROM categorie WHERE nome = ?",
                (nome_categoria,)
            )
            
            if self.cursor.fetchone():
                # OUTPUT - Errore
                print("✗ La categoria esiste già.")
            else:
                # Step 4: Inserimento della categoria (SQL INSERT)
                self.cursor.execute(
                    "INSERT INTO categorie (nome) VALUES (?)",
                    (nome_categoria,)
                )
                self.conn.commit()
                
                # OUTPUT - Successo
                print("✓ Categoria inserita correttamente.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    def visualizza_categorie(self):
        """
        Funzione ausiliaria per visualizzare tutte le categorie disponibili
        """
        try:
            self.cursor.execute("SELECT id, nome FROM categorie ORDER BY nome")
            categorie = self.cursor.fetchall()
            
            if categorie:
                print("\nCategorie disponibili:")
                print("-" * 30)
                for cat_id, nome in categorie:
                    print(f"{cat_id}. {nome}")
                print("-" * 30)
                return True
            else:
                print("\nNessuna categoria disponibile.")
                return False
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
            return False
    
    # ========================================
    # MODULO 2: INSERIMENTO SPESA
    # ========================================
    
    def inserisci_spesa(self):
        """
        MODULO 2 - Inserimento di una Spesa
        
        Obiettivo: Registrare una nuova spesa
        
        Input (da console):
        - Data (formato YYYY-MM-DD)
        - Importo
        - Nome della categoria
        - Descrizione facoltativa
        
        Elaborazione (passo per passo):
        1. Acquisizione di tutti gli input
        2. Validazione dell'importo: if (importo <= 0) → errore
        3. Verifica dell'esistenza della categoria (SQL SELECT)
        4. Inserimento della spesa (SQL INSERT con chiave esterna)
        
        Output:
        - Successo: Spesa inserita correttamente.
        - Errori: Errore: l'importo deve essere maggiore di zero.
                  Errore: la categoria non esiste.
        """
        print("\n" + "="*50)
        print("INSERIMENTO SPESA")
        print("="*50)
        
        # Verifica che esistano categorie
        if not self.visualizza_categorie():
            print("✗ Devi prima creare almeno una categoria.")
            self.pausa()
            return
        
        # STEP 1: Acquisizione di tutti gli input
        
        # Input 1: Data
        data = input("\nInserisci la data (YYYY-MM-DD) o premi INVIO per oggi: ").strip()
        if not data:
            data = datetime.now().strftime("%Y-%m-%d")
        else:
            # Validazione formato data
            try:
                datetime.strptime(data, "%Y-%m-%d")
            except ValueError:
                print("✗ Errore: formato data non valido. Usa YYYY-MM-DD.")
                self.pausa()
                return
        
        # Input 2: Importo
        importo_str = input("Inserisci l'importo: ")
        
        # Input 3: Nome della categoria
        nome_categoria = input("Inserisci il nome della categoria: ").strip()
        
        # Input 4: Descrizione facoltativa
        descrizione = input("Inserisci una descrizione (opzionale): ").strip()
        
        # STEP 2: Validazione dell'importo
        try:
            importo = float(importo_str)
            
            # if (importo <= 0) → errore
            if importo <= 0:
                print("✗ Errore: l'importo deve essere maggiore di zero.")
                self.pausa()
                return
        
        except ValueError:
            print("✗ Errore: l'importo deve essere maggiore di zero.")
            self.pausa()
            return
        
        # STEP 3: Verifica dell'esistenza della categoria (SQL SELECT)
        try:
            self.cursor.execute(
                "SELECT id FROM categorie WHERE nome = ?",
                (nome_categoria,)
            )
            risultato = self.cursor.fetchone()
            
            if not risultato:
                print("✗ Errore: la categoria non esiste.")
                self.pausa()
                return
            
            categoria_id = risultato[0]
            
            # STEP 4: Inserimento della spesa (SQL INSERT con chiave esterna)
            self.cursor.execute(
                "INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)",
                (data, importo, categoria_id, descrizione if descrizione else None)
            )
            self.conn.commit()
            
            # OUTPUT - Successo
            print("\n✓ Spesa inserita correttamente.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    # ========================================
    # MODULO 3: DEFINIZIONE BUDGET
    # ========================================
    
    def definisci_budget(self):
        """
        MODULO 3 - Definizione del Budget Mensile
        
        Obiettivo: Impostare un limite di spesa per una categoria 
                   in un determinato mese
        
        Input (da console):
        - Mese (YYYY-MM)
        - Nome della categoria
        - Importo del budget
        
        Elaborazione:
        1. Verifica che il budget sia maggiore di zero
        2. Controllo dell'esistenza della categoria
        3. Inserimento o aggiornamento del record di budget
        
        Output: Budget mensile salvato correttamente.
        """
        print("\n" + "="*50)
        print("DEFINIZIONE BUDGET MENSILE")
        print("="*50)
        
        # Verifica che esistano categorie
        if not self.visualizza_categorie():
            print("✗ Devi prima creare almeno una categoria.")
            self.pausa()
            return
        
        # INPUT
        
        # Input 1: Mese
        mese = input("\nInserisci il mese (YYYY-MM) o premi INVIO per il mese corrente: ").strip()
        if not mese:
            mese = datetime.now().strftime("%Y-%m")
        else:
            # Validazione formato mese
            try:
                datetime.strptime(mese + "-01", "%Y-%m-%d")
            except ValueError:
                print("✗ Errore: formato mese non valido. Usa YYYY-MM.")
                self.pausa()
                return
        
        # Input 2: Nome della categoria
        nome_categoria = input("Inserisci il nome della categoria: ").strip()
        
        # Input 3: Importo del budget
        importo_str = input("Inserisci l'importo del budget: ")
        
        # ELABORAZIONE
        
        # STEP 1: Verifica che il budget sia maggiore di zero
        try:
            importo_budget = float(importo_str)
            
            if importo_budget <= 0:
                print("✗ Errore: il budget deve essere maggiore di zero.")
                self.pausa()
                return
        
        except ValueError:
            print("✗ Errore: il budget deve essere maggiore di zero.")
            self.pausa()
            return
        
        # STEP 2: Controllo dell'esistenza della categoria
        try:
            self.cursor.execute(
                "SELECT id FROM categorie WHERE nome = ?",
                (nome_categoria,)
            )
            risultato = self.cursor.fetchone()
            
            if not risultato:
                print("✗ Errore: la categoria non esiste.")
                self.pausa()
                return
            
            categoria_id = risultato[0]
            
            # STEP 3: Inserimento o aggiornamento del record di budget
            self.cursor.execute(
                "INSERT OR REPLACE INTO budget (mese, categoria_id, importo) VALUES (?, ?, ?)",
                (mese, categoria_id, importo_budget)
            )
            self.conn.commit()
            
            # OUTPUT
            print("\n✓ Budget mensile salvato correttamente.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    # ========================================
    # MODULO 4: VISUALIZZAZIONE REPORT
    # ========================================
    
    def menu_report(self):
        """
        MODULO 4 - Visualizzazione dei Report
        
        Obiettivo: Visualizzare informazioni calcolate tramite interrogazioni SQL
        
        Il modulo include un sottomenu implementato tramite switch (if-elif-else)
        
        Menu dei Report:
        1. Totale spese per categoria
        2. Spese mensili vs budget
        3. Elenco completo delle spese ordinate per data
        4. Ritorna al menu principale
        """
        while True:
            self.pulisci_schermo()
            print("="*50)
            print("MENU REPORT")
            print("="*50)
            print("1. Totale spese per categoria")
            print("2. Spese mensili vs budget")
            print("3. Elenco completo delle spese ordinate per data")
            print("4. Ritorna al menu principale")
            print("="*50)
            
            scelta = input("\nInserisci la tua scelta: ").strip()
            
            # SWITCH implementato con if-elif-else
            if scelta == "1":
                self.report_totale_per_categoria()
            elif scelta == "2":
                self.report_spese_vs_budget()
            elif scelta == "3":
                self.report_elenco_spese()
            elif scelta == "4":
                break
            else:
                print("✗ Scelta non valida. Riprovare.")
                self.pausa()
    
    def report_totale_per_categoria(self):
        """
        REPORT 1: Totale delle Spese per Categoria
        
        Output (console) - esempio:
        Categoria........Totale Speso
        Alimentari.......320.50
        Trasporti........120.00
        """
        print("\n" + "="*50)
        print("TOTALE SPESE PER CATEGORIA")
        print("="*50)
        
        try:
            # Query SQL con GROUP BY e SUM
            self.cursor.execute('''
                SELECT c.nome, COALESCE(SUM(s.importo), 0) as totale
                FROM categorie c
                LEFT JOIN spese s ON c.id = s.categoria_id
                GROUP BY c.id, c.nome
                ORDER BY totale DESC
            ''')
            
            risultati = self.cursor.fetchall()
            
            if risultati:
                print(f"\n{'Categoria':<25} {'Totale Speso':>15}")
                print("-" * 50)
                for nome, totale in risultati:
                    print(f"{nome:<25} {totale:>14.2f}€")
                print("-" * 50)
            else:
                print("\n✗ Nessuna spesa registrata.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    def report_spese_vs_budget(self):
        """
        REPORT 2: Spese Mensili vs Budget
        
        Elaborazione:
        1. Calcolo del totale speso per mese e categoria (SQL)
        2. Confronto con il budget tramite if / else
        3. Visualizzazione dello stato
        
        Output (esempio):
        Mese: 2025-01
        Categoria: Alimentari
        Budget: 300
        Speso: 320
        Stato: SUPERAMENTO BUDGET
        """
        print("\n" + "="*50)
        print("SPESE MENSILI VS BUDGET")
        print("="*50)
        
        mese = input("\nInserisci il mese (YYYY-MM) o premi INVIO per il mese corrente: ").strip()
        if not mese:
            mese = datetime.now().strftime("%Y-%m")
        
        try:
            # STEP 1: Calcolo del totale speso per mese e categoria (SQL)
            self.cursor.execute('''
                SELECT 
                    c.nome,
                    b.importo as budget,
                    COALESCE(SUM(s.importo), 0) as speso
                FROM budget b
                JOIN categorie c ON b.categoria_id = c.id
                LEFT JOIN spese s ON c.id = s.categoria_id 
                    AND strftime('%Y-%m', s.data) = ?
                WHERE b.mese = ?
                GROUP BY c.id, c.nome, b.importo
            ''', (mese, mese))
            
            risultati = self.cursor.fetchall()
            
            if risultati:
                print(f"\n{'='*50}")
                
                for nome, budget, speso in risultati:
                    # OUTPUT formato richiesto
                    print(f"\nMese: {mese}")
                    print(f"Categoria: {nome}")
                    print(f"Budget: {budget:.0f}")
                    print(f"Speso: {speso:.0f}")
                    
                    # STEP 2 e 3: Confronto con il budget tramite if/else
                    if speso > budget:
                        print("Stato: SUPERAMENTO BUDGET")
                    else:
                        rimanente = budget - speso
                        print(f"Stato: OK (Rimanente: {rimanente:.2f}€)")
                    
                    print("-" * 50)
            else:
                print(f"\n✗ Nessun budget definito per il mese {mese}.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    def report_elenco_spese(self):
        """
        REPORT 3: Elenco Completo delle Spese Ordinate per Data
        
        Output (esempio):
        Data       Categoria    Importo  Descrizione
        --------------------------------------------------------------
        2025-01-15 Alimentari   25.00    Pranzo
        """
        print("\n" + "="*50)
        print("ELENCO COMPLETO DELLE SPESE")
        print("="*50)
        
        try:
            # Query SQL con ORDER BY data
            self.cursor.execute('''
                SELECT s.data, c.nome, s.importo, s.descrizione
                FROM spese s
                JOIN categorie c ON s.categoria_id = c.id
                ORDER BY s.data DESC
            ''')
            
            risultati = self.cursor.fetchall()
            
            if risultati:
                print(f"\n{'Data':<12} {'Categoria':<20} {'Importo':>10} {'Descrizione':<30}")
                print("-" * 80)
                
                totale = 0
                for data, categoria, importo, descrizione in risultati:
                    desc = descrizione if descrizione else "-"
                    print(f"{data:<12} {categoria:<20} {importo:>9.2f}€ {desc:<30}")
                    totale += importo
                
                print("-" * 80)
                print(f"{'TOTALE GENERALE':<32} {totale:>9.2f}€")
            else:
                print("\n✗ Nessuna spesa registrata.")
        
        except sqlite3.Error as e:
            print(f"✗ Errore nel database: {e}")
        
        self.pausa()
    
    # ========================================
    # MENU PRINCIPALE
    # ========================================
    
    def menu_principale(self):
        """
        Visualizza e gestisce il menu principale
        
        Implementato con:
        - cout (print)
        - cin (input)
        - switch (if-elif-else)
        - ciclo iterativo (while)
        """
        while True:
            self.pulisci_schermo()
            print("="*50)
            print("SISTEMA SPESE PERSONALI")
            print("="*50)
            print("1. Gestione Categorie")
            print("2. Inserisci Spesa")
            print("3. Definisci Budget Mensile")
            print("4. Visualizza Report")
            print("5. Esci")
            print("="*50)
            
            scelta = input("\nInserisci la tua scelta: ").strip()
            
            # SWITCH implementato con if-elif-else
            if scelta == "1":
                self.gestione_categorie()
            elif scelta == "2":
                self.inserisci_spesa()
            elif scelta == "3":
                self.definisci_budget()
            elif scelta == "4":
                self.menu_report()
            elif scelta == "5":
                print("\n✓ Grazie per aver utilizzato il Sistema Spese Personali!")
                print("Arrivederci!")
                break
            else:
                print("✗ Scelta non valida. Riprovare.")
                self.pausa()
    
    def avvia(self):
        """
        Avvia l'applicazione
        """
        self.pulisci_schermo()
        print("\n" + "="*50)
        print("BENVENUTO NEL SISTEMA DI GESTIONE")
        print("SPESE PERSONALI E DEL BUDGET")
        print("="*50)
        print("\nProgetto Finale - Fondamenti di Informatica")
        print("Repository: https://github.com/gioelemocci06/Fondamenti-di-informatica-")
        self.pausa()
        
        try:
            self.menu_principale()
        finally:
            self.chiudi_connessione()


# ========================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# ========================================

if __name__ == "__main__":
    sistema = SistemaSpese()
    sistema.avvia()