# Requisiti Funzionali - C'è PosTo

## Descrizione Generale
L'applicazione web consente agli studenti del Politecnico di Torino di prenotare aule studio disponibili, scegliendo una data e una fascia oraria.  
Gli utenti devono registrarsi autonomamente sull'applicazione per poter utilizzare il servizio.

## Requisiti Funzionali

### RF1 - Registrazione e Autenticazione
- L'utente deve potersi registrare creando un account personale, fornendo:
  - Nome e cognome.
  - Email istituzionale (@polito.it).
  - Password.
- Dopo la registrazione, l'utente deve potersi autenticare inserendo email e password.
- In caso di credenziali errate, deve essere mostrato un messaggio di errore.
- Deve essere previsto un sistema di recupero password.

### RF2 - Visualizzazione Aule Disponibili
- Dopo l'autenticazione, l'utente deve poter visualizzare:
  - La lista delle aule studio disponibili.
  - Per ciascuna aula: la capienza massima e l'ubicazione (edificio, piano).
  - Le fasce orarie disponibili per la data selezionata.

### RF3 - Selezione Data e Fascia Oraria
- L'utente deve poter selezionare una data tramite un calendario.
- L'utente deve poter selezionare una o più fasce orarie disponibili per l'aula scelta.

### RF4 - Prenotazione Aula
- L'utente deve poter confermare la prenotazione dell'aula selezionata per la data e la fascia oraria desiderata.
- Alla conferma, il sistema deve:
  - Registrare la prenotazione associandola all'utente.
  - Aggiornare la disponibilità dell'aula.
  - Mostrare un messaggio di conferma.

### RF5 - Visualizzazione Prenotazioni Personali
- L'utente deve poter visualizzare l'elenco delle proprie prenotazioni future e passate.
- Per ogni prenotazione devono essere mostrati:
  - Aula prenotata.
  - Data.
  - Fascia oraria.

### RF6 - Cancellazione Prenotazione
- L'utente deve poter cancellare una prenotazione prima dell'orario di inizio previsto.
- In caso di cancellazione, il sistema deve liberare la disponibilità dell'aula.

### RF7 - Gestione Limiti di Prenotazione
- È possibile limitare:
  - Il numero massimo di prenotazioni attive per utente.
  - La durata massima prenotabile per singola giornata (es. massimo 4 ore).

### RF8 - Notifiche (NO)
- Il sistema deve inviare una email di conferma all'utente al momento della prenotazione.
- Il sistema deve inviare un promemoria il giorno prima della prenotazione.

## Note Aggiuntive
- L'applicazione deve essere responsive e utilizzabile da dispositivi mobili.