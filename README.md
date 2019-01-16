# Trivia-Project-Web-ProgIK
Code for the trivia webpage project /Chris/ Jesper / Dido.
 Controller / Paginas / application.py


Voorpagina	-	GET
Login		-	GET+POST
Registratie	-	GET+POST
Index		-	GET+POST
Vragen		-	GET+POST
Uitslag		-	GET
Top 10		-	GET
Compare	-	GET+POST
Compared	-	GET+POST
Apology	-	GET

Model / functions.py

login()		-	Laat de gebruiker inloggen
register()	-	Laat de gebruiker registreren + logt in
l()		-	Gheckt of de gebruiker ingelogt is
stats()		-	Geeft aantal vragen correct + % correct
ranks()		-	Geeft de plaats in de scorelijsten aan van de gebruiker in Nr en %
questions()	-	Genereert de lijst van vragen
store()		-	Slaat de aangepaste vragen informatie van de gebruiker op in de database
top-nr()	-	Geeft de top 10 mbt. vragen correct van alle gebruikers
top-%()	-	Geeft de top 10 mbt. percentage correct van alle gebruikers
compare()	-	Geeft de stats van de gebruiker + die van een geselecteerde andere gebruiker
result()		-	Controleert antwoorden van de gebruiker + geeft correcte antwoorden
logout()	-	Logt de gebruiker uit

Databases

Externe Database	-	De bron van onze vragen
users			-	ID Nr + naam + password hash van elke gebruiker
stats			-	ID Nr + aantal vragen beatwoord + aantal vragen goed (+ punten)





