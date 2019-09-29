# Praćenje volonterskih sati KSET-ovaca
Ova aplikacija je originalno stvorena radi olakšanja praćenja volonterskih sati članova KSET-a Foto sekcije.
Nedugo nakon početka razvoja se skužilo da se funkcionalnosti aplikacije mogu generalizirati za praćenje sati
volontiranja članova iz svih sekcija zasebno.

Ova aplikacija može služiti za:
>Vođenje baze članova

>Vođenje baze aktivnosti sekcija

>Vođenje baze dolaznosti članova na aktivnosti

>Pregled statistika aktivnosti člana

>Export statistika aktivnosti sekcije

>Arhiviranje članova

Da bi se moglo koristit aplikaciju, potrebno je imati korisnički račun koji se dobije od strane Administratora.

## Kratki opis sustava
Aplikacija je razvijena u jeziku Python verzije 3.6. Za stvaranje korisničkog web sučelja je korišten 
Flask framework, HTML5, Javascript, JQuery i nešto sitno CSS-a.

Baza članova, aplikacija, sati i svega ostaloga je ostvarena koristeći SQLite3 modul.

Za provjeru lozinke kod ulogiravanja se koristi modul werkzeug.security.

Sve metode koje se bave manipulacijom baze podataka su sadržane u DatabaseController.py modulu.

Glavna skripta preko koje se aplikacija pokreće je web_app.py

## Korištenje aplikacije

Ukoliko želiš nešto napraviti a nisi siguran (ili neznaš) kako, ovdje vjerojatno možeš naći odgovor.
U nastavku su dani odgovori na moguća pitanja oko korištenja programa.

Ako ispod ne postoji odgovor na tvoje pitanje, slobodno javi pa će se popis ažurirati :) .

### Pridruživanje člana sekciji
Pridruživanje člana započinje njegovom pretragom po broju članske iskaznice.
Ukoliko broj članske iskaznice nije poznat, javi se savjetniku sekcije iz koje se član pridružuje koji 
može vidjeti broj članske iskaznice na listi članova.

Člana se može pridružiti samo u sekciju koja je povezana sa ulogiranim korisničkim računom.

### Sudjelovanje člana u timovima
Timovi se u suštini ponašaju kao sekcije pa tako sudjelovanje člana u timu (npr. PR, dizajn itd.) 
se definira preko pridruživanja člana tom timu. Pridruživanje člana timu se obavlja sa računa koji je 
definiran za taj tim.

### Tip aktivnosti ne postoji za aktivnost koju stvaram
Novi tip aktivnosti se može stvoriti preko opcije Aktivnost -> Dodaj tip aktivnosti.
Stvoreni tip aktivnosti se veže uz sekciju koja je definirana za ulogirani račun.
Administrator može stvoriti tip aktivnosti koji će biti vidljiv svim sekcijama.

### Treba dodati novi tim
Novi tim se (zasad) mora dodati ručno unutar samog koda. 
Osoba koja ima pristup kodu treba unutar Utilities.py skripte pod riječnik teams dodati željeni tim. 
Uz to u modulu constants je potrebno stvoriti Konstantu koja će reprezentirati taj tim na web sučelju.

### Treba exportati podatke o volontiranju članova
Svaki savjetnik može eksportati volonterske sate u željenom intervalu za svoju sekciju odlaskom na 
intervalnu statistiku, odabirom intervala te pritiskom na gumb export. 
Sam export se zapisuje u TXT datoteku koju se može preuzeti na vlastiti komp.
Radi lijepšeg pregleda preporuča se otvoriti datoteku sa naprednijim txt editorom (npr. Notepad++)

Administrator može napraviti eksport svih sekcija odjednom.

### Postoji problem s aplikacijom
Ako se aplikacija ruši ili postoji bug, molim te da ga prijaviš na GitHub repozitorij preko raise Issue opcije.
Link na repozitorij je : https://github.com/mlaggi0/VolonterskiSati

