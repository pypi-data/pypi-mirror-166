
Expects a file in CSV-CAMT-Format, with the following columns:

- Auftragskonto
- Buchungstag
- Valutadatum
- Buchungstext
- Verwendungszweck
- Glaeubiger ID
- Mandatsreferenz
- Kundenreferenz (End-to-End)
- Sammlerreferenz
- Lastschrift Ursprungsbetrag
- Auslagenersatz Ruecklastschrift
- Beguenstigter/Zahlungspflichtiger
- Kontonummer/IBAN
- BIC (SWIFT-Code)
- Betrag
- Waehrung
- Info

Outputs a normal CSV file with the following columns:

- Date
- Deposit
- Withdrawal
- Description
- Reference Number
- Bank Account
- Currency
