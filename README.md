# Trivia-Project-Web-ProgIK
Code for the trivia webpage project /Chris/ Jesper / Dido.

### Voorstel

Wij willen een Trivia spel gaan maken dat gaat over landen. De gebruikers beantwoorden vragen in sets van 10. De vragen worden een voor een aan de gebruiker getoond. Na het beantwoorden van een vraag komt de volgende vraag, totdat alle vragen beantwoord zijn. Aan het einde van de set van 10 komt er een overzicht waarin staat welke vragen goed en fout zijn beantwoord waarbij het goede antwoord erbij wordt vermeld.
Gebruikers komen in top 10 lijsten te staan op basis van aantal goede vragen en percentage goed beantwoorde vragen. Verder willen we een zoekfunctie maken binnen de ranglijst zodat je onderling kunt concurreren met je vrienden en/of vijanden, ook als deze niet in de top 10 staan.

### Controller


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

### Views
<img src="https://i.imgur.com/yDj1ZRy.png" width="200"> <br>
#### frontpage
<img src="https://i.imgur.com/S79mOVy.png" width="200"> <br>
#### login-page
<img src="https://i.imgur.com/oCVGGU4.png" width="200"> <br>
### register-page
<img src="https://i.imgur.com/sIfgpEI.png" width="200"> <br>
### index
<img src="https://i.imgur.com/ZpZ4hMQ.png" width="200"> <br>
### vragen
<img src="https://i.imgur.com/YtBoNwt.png" width="200"> <br>
### resultaten
<img src="https://i.imgur.com/YNVrxN7.png" width="200"> <br>
### vergelijk
<img src="https://i.imgur.com/mdYQ6Qq.png" width="200"> <br>
### top10
<img src="https://i.imgur.com/0EDiLhv.png" width="200"> <br>


### Models/helpers

login()		-	Laat de gebruiker inloggen<br>
register()	-	Laat de gebruiker registreren + logt in<br>
l()		-	Gheckt of de gebruiker ingelogt is<br>
stats()		-	Geeft aantal vragen correct + % correct<br>
ranks()		-	Geeft de plaats in de scorelijsten aan van de gebruiker in Nr en %<br>
questions()	-	Genereert de lijst van vragen<br>
store()		-	Slaat de aangepaste vragen informatie van de gebruiker op in de database<br>
top-nr()	-	Geeft de top 10 mbt. vragen correct van alle gebruikers<br>
top-%()	-	Geeft de top 10 mbt. percentage correct van alle gebruikers<br>
compare()	-	Geeft de stats van de gebruiker + die van een geselecteerde andere gebruiker<br>
result()		-	Controleert antwoorden van de gebruiker + geeft correcte antwoorden<br>
logout()	-	Logt de gebruiker uit<br>

### Databases

Externe Database	-	De bron van onze vragen<br>
users			-	ID Nr + naam + password hash van elke gebruiker<br>
stats			-	ID Nr + aantal vragen beatwoord + aantal vragen goed (+ punten)<br>


### Plugins en frameworks + documentatie
flask http://flask.pocoo.org/<br>
passlib. https://passlib.readthedocs.io/en/stable/lib/passlib.apps.html/<br>
sql https://www.w3schools.com/sql/<br>

<br>

