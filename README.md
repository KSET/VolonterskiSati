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

Da bi se moglo koristit aplikaciju, potrebno je registrirati korisnički račun.

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

### Nemogu se registrirati
Za uspješnu registraciju potrebno je znati pozivni kod koji se može dobiti od savjetnika svoje sekcije.
Razina dobivene ovlasti će odgovarati upisanom pozivnom kodu.

### Import podataka
Import podataka se vrši preko komandne linije koristeći skripte import_\<ime_baze>.
Trenutno postoje dvije skripte za import podataka:

    import_members
    
Kod pokretanja skripte je potrebno predati putanju do csv datoteke koja sadrži podatke za import:
    
    python import_members <putanja_do_datoteke.csv>

#### Format podataka za import
Kod importa članova potrebno je osigurati sljedeće:

    - Datoteka mora biti u csv formatu.
    - Import podržava nazive stupaca sljedećih imena (redoslijed u tablici nije bitan):
        ime
        prezime
        nadimak
        boja_iskaznice (plava, narancasta ili crvena)
        datum_rodenja	
        email	
        mobitel	
        datum_uclanjenja	
        oib	
        aktivan (bit koji označava da li je član trenutno aktivan)
        section	
        broj_iskaznice
    - Nedostatak bilo kojeg* od gore navedenih stupaca će biti zamijenjen vrijednošću '-'
    - *Nedostatak polja broj_iskaznice (prazno polje) će generirati novi broj iskaznice u ovisnosti o zadnjem broju u bazi.
        TIP: Ako broj iskaznice nije trenutno poznat moguće je u datoteci staviti "-" pa kasnije izmjeniti. 
    - Format zapisa datuma rođenja i datuma učlanjenja mora biti isti. Po defaultu se uzima "godina-mjesec-dan"
    no moguće je unutar kod import skripte primjeniti custom format.

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
Sam export se zapisuje u CSV datoteku koju se može preuzeti na vlastiti komp.

TIP: Ako podaci unutar CSV datoteke budu u jednom stupcu, unutar excela je moguće pravilno ih 
rasporediti po zadanom delimiteru (",") tako da se izabere stupac sa podacima, odabere opcija Data -> text to columns
te prate upute za razbijanje teksta u stupce. Kod delimitera je potrebno odabrati znak koji odvaja zasebne stupce
(po defaultu je to zarez).

Administrator može napraviti eksport svih sekcija odjednom.

### Postoji problem s aplikacijom
Ako se aplikacija ruši ili postoji bug, molim te da ga prijaviš na GitHub repozitorij preko raise Issue opcije.
Link na dizanje novog Issua na repozitoriju je : https://github.com/mlaggi0/VolonterskiSati/issues/new

## TODO lista

- [ ] Import članova/aktivnosti
- [ ] Paginacija kod izlistavanja članova i aktivnosti
- [ ] Optimizacija kontrolera baze podataka