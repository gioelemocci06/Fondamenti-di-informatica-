-- =====================================================
-- SCRIPT DI CREAZIONE DATABASE
-- Sistema di Gestione delle Spese Personali e del Budget
-- =====================================================

-- (Se usi solo SQLite non serve CREATE DATABASE, il file .db
-- viene creato dallo script Python.)

-- Prima rimuovo eventuali tabelle esistenti (ordine corretto
-- per rispettare le foreign key)
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS spese;
DROP TABLE IF EXISTS categorie;

-- =========================================
-- TABELLA: categorie
-- =========================================
CREATE TABLE categorie (
    id_categoria     INTEGER PRIMARY KEY AUTOINCREMENT,   -- PRIMARY KEY
    nome             VARCHAR(100) NOT NULL UNIQUE         -- NOT NULL + UNIQUE
);

-- Vincoli espliciti:
-- PRIMARY KEY: id_categoria
-- NOT NULL: nome
-- UNIQUE: nome

-- =========================================
-- TABELLA: spese
-- =========================================
CREATE TABLE spese (
    id_spesa         INTEGER PRIMARY KEY AUTOINCREMENT,   -- PRIMARY KEY
    data_spesa       DATE NOT NULL,                       -- NOT NULL
    importo          DECIMAL(10,2) NOT NULL CHECK (importo > 0),  -- NOT NULL + CHECK
    id_categoria     INTEGER NOT NULL,                    -- NOT NULL (FOREIGN KEY)
    descrizione      VARCHAR(255),
    
    CONSTRAINT fk_spese_categoria
        FOREIGN KEY (id_categoria)                        -- FOREIGN KEY
        REFERENCES categorie(id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Vincoli espliciti:
-- PRIMARY KEY: id_spesa
-- NOT NULL: data_spesa, importo, id_categoria
-- CHECK: importo > 0
-- FOREIGN KEY: id_categoria → categorie(id_categoria)

-- =========================================
-- TABELLA: budget
-- =========================================
CREATE TABLE budget (
    id_budget        INTEGER PRIMARY KEY AUTOINCREMENT,   -- PRIMARY KEY
    mese             CHAR(7) NOT NULL,                    -- Formato previsto: 'YYYY-MM' (NOT NULL)
    id_categoria     INTEGER NOT NULL,                    -- NOT NULL (FOREIGN KEY)
    importo_budget   DECIMAL(10,2) NOT NULL CHECK (importo_budget > 0), -- NOT NULL + CHECK
    
    CONSTRAINT uq_budget_mese_categoria
        UNIQUE (mese, id_categoria),                      -- UNIQUE (mese, categoria)
    
    CONSTRAINT fk_budget_categoria
        FOREIGN KEY (id_categoria)                        -- FOREIGN KEY
        REFERENCES categorie(id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Vincoli espliciti:
-- PRIMARY KEY: id_budget
-- NOT NULL: mese, id_categoria, importo_budget
-- CHECK: importo_budget > 0
-- UNIQUE: (mese, id_categoria)
-- FOREIGN KEY: id_categoria → categorie(id_categoria)

-- =====================================================
-- INSERIMENTO DATI DI ESEMPIO
-- =====================================================

-- =========================================
-- CATEGORIE
-- =========================================
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Svago');
INSERT INTO categorie (nome) VALUES ('Bollette');

-- =========================================
-- SPESE (usa gli id auto-generati delle categorie)
-- Supponendo:
-- 1 = Alimentari, 2 = Trasporti, 3 = Svago, 4 = Bollette
-- =========================================

-- SPESE ALIMENTARI (id_categoria = 1)
INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-05',  45.50, 1, 'Spesa supermercato');

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-10',  25.00, 1, 'Pranzo veloce');

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-20', 150.00, 1, 'Spesa mensile grande');

-- SPESE TRASPORTI (id_categoria = 2)
INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-03',  50.00, 2, 'Benzina auto');

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-15',  35.00, 2, 'Biglietto treno');

-- SPESE SVAGO (id_categoria = 3)
INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-12',  20.00, 3, 'Cinema');

INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-25',  60.00, 3, 'Cena con amici');

-- SPESE BOLLETTE (id_categoria = 4)
INSERT INTO spese (data_spesa, importo, id_categoria, descrizione)
VALUES ('2025-01-08',  80.00, 4, 'Bollette luce/gas');

-- =========================================
-- BUDGET MENSILI
-- =========================================

-- Budget per gennaio 2025
INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-01', 1, 300.00);   -- Alimentari

INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-01', 2, 120.00);   -- Trasporti

INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-01', 3, 100.00);   -- Svago

INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-01', 4,  90.00);   -- Bollette

-- Budget per febbraio 2025 (solo alcuni esempi)
INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-02', 1, 280.00);   -- Alimentari

INSERT INTO budget (mese, id_categoria, importo_budget)
VALUES ('2025-02', 2, 100.00);   -- Trasporti;