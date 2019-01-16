# Trivia-Project-Web-ProgIK
Code for the trivia webpage project /Chris/ Jesper / Dido.  

### Controller / Paginas / application.py


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

### Model / functions.py

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



