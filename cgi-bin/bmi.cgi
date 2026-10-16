#!/usr/bin/env python3
import os
import sys
from urllib.parse import parse_qs
import html

print("Content-Type: text/html; charset=utf-8")
print()

if os.environ.get("REQUEST_METHOD") == "POST":
    length = int(os.environ.get("CONTENT_LENGTH", 0))
    data = sys.stdin.read(length)
    form = parse_qs(data)

    name = html.escape(form.get("name", [""])[0].strip())

    try:
        gewicht = float(form.get("gewicht", [""])[0])
        groesse = float(form.get("groesse", [""])[0])

        if not name or gewicht <= 0 or groesse <= 0:
            raise ValueError

        bmi = gewicht / ((groesse / 100) ** 2)

        if bmi < 18.5:
            bewertung = "Untergewicht"
        elif bmi < 25:
            bewertung = "Normalgewicht"
        elif bmi < 30:
            bewertung = "Übergewicht"
        else:
            bewertung = "Adipositas"

        ergebnis = (
            f"<h2>Hallo {name}!</h2>"
            f"<p>Dein BMI beträgt: <strong>{bmi:.1f}</strong></p>"
            f"<p>Einordnung: {bewertung}</p>"
        )

    except (ValueError, TypeError):
        ergebnis = (
            "<p class='error'>"
            "Bitte gib einen Namen, ein gültiges Gewicht "
            "und eine gültige Größe ein.</p>"
        )
else:
    ergebnis = "<p>Bitte nutze das Formular zur BMI-Berechnung.</p>"

print("""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BMI-Ergebnis</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div class="container">
<h1>Dein Ergebnis</h1>
""")

print(ergebnis)

print("""
<p><a href="../index.html">Zurück zum Rechner</a></p>
</div>
</body>
</html>
""")

