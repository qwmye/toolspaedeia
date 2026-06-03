# Structura Lucrării de Licență - Toolspaedeia

## 1. Rezumat
Lucrarea descrie procesul de dezvoltare pentru ToolsPaedeia, o platformă de Mobile Learning (M-Learning) care prioritizează accesul la conținut educațional în detrimentul complexității vizuale. Sistemul este construit pe o arhitectură "lean", utilizând Django, HTMX și PicoCSS, cu implementarea de Progressive Web App (PWA) pentru suportul de acces offline. Această abordare a optimizat performanța de randare pe dispozitive mobile și a asigurat portabilitatea datelor. Rezultatul este un mediu de învățare cu timp de răspuns redus și un model de acces simplificat, validat prin teste de integrare și analiza performanței în mediul de producție.

## 2. Cuprins
[TOC]

## 3. Abrevieri
M-Learning - Mobile Learning
PWA - Progressive Web App
HTMX - Hypermedia for HTML
HATEOAS - Hypermedia as the Engine of Application State
AJAX - Asynchronous JavaScript and XML
MVT - Model-View-Template
MVC - Model-View-Controller
API - Application Programming Interface
LMS - Learning Management Systems
SPA - Single Page Application
ER - Entity-Relationship

## 4. Lista tabelelor și figurilor
[Placeholder: Listă a tuturor figurilor și tabelelor utilizate în lucrare]

## 5. Introducere
Trecerea sistemelor de învățare de la platformele de management al învățării (LMS), precum Moodle, către aplicații de divertisment educațional ("edutainment") a pus accentul pe gamificare și interactivitate. Lucrarea propune dezvoltarea platformei Toolspaedeia, un mediu de învățare orientat către accesibilitatea conținutului și simplitatea interfeței.

Proiectul utilizează paradigma învățării mobile, fragmentând cursurile în lecții scurte pentru a facilita accesul asincron. Din punct de vedere tehnic, Toolspaedeia utilizează randarea pe server pentru a reduce consumul de resurse pe dispozitivele mobile, evitând complexitatea interfețelor de tip Single Page Application (SPA). Pentru a preveni dependența de furnizor (vendor lock-in) și a asigura portabilitatea datelor, platforma utilizează standardul Markdown.

Obiectivele principale includ implementarea accesului offline prin tehnologia PWA, integrarea unui sistem de plăți securizat și optimizarea administrării resurselor prin analiză statică și Machine Learning.

Metodologia de lucru a fost iterativă, cu etape de analiză, proiectare, implementare și testare, urmate de evaluări periodice în mediul de producție.

Lucrarea este structurată în șase capitole:
- **Capitolul 1: Metodologia de Lucru și Instrumentarul Tehnologic**, prezentând pașii de dezvoltare, standardele de calitate și instrumentele utilizate.
- **Capitolul 2: Fundamente Teoretice**, analizând conceptele de PWA, Lean Frontend, Markdown și Machine Learning.
- **Capitolul 3: Analiza de Business și Cerințe**, descryzând contextul pieței, nevoile utilizatorilor și modelul economic.
- **Capitolul 4: Proiectarea Sistemului**, dedicat arhitecturii MVT, modelării datelor și fluxurilor de lucru.
- **Capitolul 5: Implementarea Sistemului**, detaliind procesul de codare, integrarea API-urilor de plăți și deployment-ul.
- **Capitolul 6: Evaluarea și Validarea Calității**, axat pe strategia de testare, acoperirea codului și performanța sistemului.

## 6. Capitole

### Capitolul 1: Metodologia de Lucru și Instrumentarul Tehnologic
#### 1.1. Metodologia de Dezvoltare
Realizarea platformei Toolspaedeia a urmat o metodologie de dezvoltare iterativă, bazată pe cicluri de analiză, proiectare, implementare și validare. Această abordare a permis rafinarea interfeței și a funcționalităților pe măsură ce performanța era evaluată în mediul de producție.

Procesul de dezvoltare a fost structurat în patru faze principale. Prima etapă a constatat stabilirea modelelor fundamentale pentru Cursuri și Module, împreună cu implementarea unui sistem de urmărire a progresiei care permite marcarea modulelor ca fiind finalizate.

`[DIAGRAMA: Fluxul de dezvoltare iterativ - Analiză -> Proiectare -> Implementare -> Validare]`

A doua fază s-a concentrat pe sistemul de livrare a conținutului, utilizând randarea pe server pentru a optimiza timpul de răspuns. În această etapă s-a implementat motorul de randare Markdown, suportul pentru MathJax și integrarea documentelor PDF, alături de un sistem de Quiz-uri cu logică de calcul a notelor și limitare a încercărilor.

`[Screencapture: Interfața de randare a unui modul cu elemente interactive]`

Treieta fază a vizat personalizarea și monetizarea, prin implementarea stratului de preferințe al utilizatorului și a sistemului de achiziții. Pentru a evita abonamentele recurente, s-a integrat API-ul Stripe pentru plăți unice, utilizând webhook-uri pentru sincronizarea stării tranzacțiilor în baza de date locală.

`[DIAGRAMA: Fluxul de achiziție a unui curs - de la selectare la confirmarea plății]`

Ultima etapă a cuprins optimizarea, inteligența sistemului și deployment-ul. S-a implementat un sistem de sugestii automate pentru etichete bazat pe `scikit-learn` și s-a configurat platforma ca Progressive Web App (PWA) pentru suportul offline. Validarea finală a fost realizată prin teste de integrare și deployment pe PythonAnywhere.

`[TABEL: Indicatori de performanță și acoperire de cod înainte și după optimizare]`

Această progresie a validat ipoteza de start: o arhitectură minimalistă, care prioritizează randarea pe server și standardele deschise, oferă o experiență de învățare eficientă pe dispozitive mobile.

#### 1.2. Standarde de Calitate și Analiză Statică
Pentru a reduce datoria tehnică și a asigura stabilitatea mediului de execuție, s-a implementat un flux de analiză statică și gestionare a dependențelor.

Determinismul mediului de lucru a fost realizat prin utilizarea instrumentului `uv`, care utilizează un fișier de lock pentru a fixa versiunile exacte ale tuturor librăriilor. Această abordare, completată de adoptarea standardului `pyproject.toml` pentru centralizarea configurării, elimină riscul de regresii între mediile de dezvoltare și producție și simplifică administrarea proiectului.

`[TABEL: Comparație între abordarea tradițională (requirements.txt) și cea modernă (pyproject.toml + lock file)]`

Controlul stilului de codare a fost automatizat prin `ruff`, care consolidează funcționalitățile de linting și formatare într-un singur instrument optimizat. Pentru stratul de prezentare, s-a integrat `djlint`, asigurând respectarea standardelor de structură și indentare în template-urile Django, care altfel ar fi fost ignorate de linterele standard.

Pentru forțarea acestor standarde, a fost implementat framework-ul `pre-commit`, care execută automat instrumentele de analiză (`ruff`, `djlint`) înainte de fiecare commit. Această integrare în fluxul de versionare previne includerea codului non-conform în repository, asigurând o calitate constantă a bazei de cod.

Sistemul de validare automatizat a permis relocarea atenției de la aspectele de formatare către implementarea logică și optimizarea performanței, asigurând o bază de cod uniformă și mentenanabilă.

#### 1.3. Tehnologii Specifice
- **Django:** Framework web Python de înaltă productivitate, utilizat pentru backend și administrare. [https://www.djangoproject.com/]
- **HTMX:** Librărie care permite accesul la AJAX, CSS Transitions, WebSockets direct în HTML, reducând nevoia de JavaScript complex. [https://htmx.org/]
- **Pico CSS:** Framework CSS minimalist, optimizat pentru performanță și accesibilitate. [https://picocss.com/]
- **Stripe API:** Platformă de procesare a plăților pentru integrarea securizată a tranzacțiilor. [https://stripe.com/]
- **Scikit-Learn:** Librărie de Machine Learning în Python, utilizată pentru clasificarea textului și sugestii de tag-uri. [https://scikit-learn.org/]
- **uv:** Instrument modern de gestionare a pachetelor Python, optimizat pentru viteză și determinism. [https://github.com/astral-sh/uv]
- **Ruff:** Linter și formatter de cod Python scris în Rust pentru analiză statică rapidă. [https://github.com/astral-sh/ruff]
- **PythonAnywhere:** Serviciu de găzduire specializat pentru aplicații Python/Django. [https://www.pythonanywhere.com/]
- **WebTest:** Librărie de testare a aplicațiilor WSGI fără a porni un server HTTP dedicat. [https://docs.pylonsproject.org/projects/webtest/]

---

### Capitolul 2: Fundamente Teoretice
#### 2.1. Aplicațiile Web Progresive (PWA)
Aplicațiile Web Progresive (PWA) permit aplicațiilor web să imite comportamentul aplicațiilor native, eliminând necesitatea instalării printr-un magazin de aplicații. Elementele critice sunt manifestul aplicației (`manifest.json`) și Service Worker-ul.

În contextul educațional, această tehnologie răspunde necesității de a integra învățarea în activitățile cotidiene. Așa cum a fost subliniat de Butoi, Tomai și Mocean (2013), M-Learning este tratat ca parte a paradigmei învățării omniprezente (ubiquitous learning) și reprezintă o extensie pervasivă a tehnologiilor de E-Learning. Service Worker-ul rulează în fundal, independent de pagina web, și acționează ca un proxy între browser și rețeaua. Această arhitectură permite implementarea strategiei de caching pentru resursele statice (CSS, JS, imagini), asigurând funcționarea platformei în absența conexiunii la internet. Pentru Toolspaedeia, această capabilitate permite accesul la lecțiile descărcate anterior, eliminând dependența de o conexiune stabilă la rețea.

#### 2.2. Paradigma "Lean Frontend"
Arhitecturile de tip Single Page Application (SPA) transferă o mare parte din procesarea logică și randarea interfeței pe partea client. Această abordare conduce la dimensiuni mari ale bundle-ului de cod, crescând timpul de încărcare și consumul de memorie pe dispozitivele mobile.

Toolspaedeia adoptă o paradigmă "lean", bazată pe principiul HATEOAS. Această alegere este motivată de necesitatea de a combate complexitatea redundantă în dezvoltarea software; după cum observă Thomas (2025), dezvoltarea software este intrinsec complexă, însă tendința actuală este de a o face, în plus de aceasta, și complicată. În locul schimbului de date JSON și randării pe client, se utilizează HTMX pentru a trimite fragmente de HTML direct în DOM. Această abordare reduce cantitatea de JavaScript executată pe dispozitiv, mutând complexitatea procesării pe server, unde resursele sunt mai stabile, evitând astfel crearea unor sisteme "grele" care consumă resurse excesive fără a aduce un beneficiu proporțional în experiența de utilizare.

Sistematizarea vizuală este realizată prin Pico CSS, o abordare minimalistă bazată pe elementele HTML semantice și un set redus de clase de utilitate. Această decizie minimizează dimensiunea payload-ului CSS și accelerează randarea paginii.

#### 2.3. Randarea Conținutului și Componentele de Interfață
Sistemul utilizează un motor de randare pe server (Server-Side Rendering), unde template-urile sunt procesate pentru a genera HTML final înainte de a fi trimise către client. Această abordare asigură un timp de primă pictare (First Contentful Paint) rapid, esențial pentru experiența de utilizare pe dispozitive mobile. Implementarea se aliniază cu principiile aplicațiilor bazate pe hipermedia, care, conform lui Volkmann (2025), permit construirea de interfețe care oferă o experiență de utilizare excelentă în timp ce minimizează complexitatea generală a sistemului.

O particularitate a implementării este utilizarea fragmentelor de template reutilizabile. În loc să se definească rute separate pentru încărcarea inițială a unei pagini și pentru actualizările parțiale solicitate prin HTMX, sistemul utilizează același fragment de cod pentru ambele cazuri. Această abordare transformă fragmentul într-o componentă cu "auto-refresh", care definește propria structură de actualizare. Prin acest mecanism, se asigură consistența vizuală între prima încărcare și interacțiunile ulterioare, reducând în același timp redundanța codului.

#### 2.4. Procesarea Limbajelor de Marcare și Portabilitatea Datelor
Alegerea formatului de stocare a conținutului educațional a fost influențată de nevoia de a evita "vendor lock-in" (dependența de un singur furnizor de software). În locul bazelor de date proprietare sau a formatelor complexe, Toolspaedeia utilizează Markdown.

Această decizie se aliniază cu filosofia "Plain Text" propagată de instrumente de gestionare a cunoșințelor precum **Obsidian** și **Bear**. Aceste aplicații demonstrează că utilizatorii preferă controlul total asupra datelor, stocându-le în fișiere text simple care pot fi citite de orice editor, independent de software-ul utilizat pentru crearea lor. Prin utilizarea Markdown, conținutul cursurilor rămâne interoperabil și portabil.

Procesul de randare este realizat prin biblioteca `mistune`, care transformă sintaxa Markdown în HTML valid pe server, asigurând că utilizatorul final primește un document optimizat, fără a necesita procesare suplimentară pe dispozitiv.

#### 2.5. Introducere în Machine Learning pentru Clasificarea Datelor
Pentru a optimiza organizarea conținutului, platforma implementează un sistem de sugestii automate pentru etichete (tags). Acest proces se bazează pe procesarea limbajului natural (NLP) și utilizarea reprezentărilor semantice (embeddings).

Sistemul a evoluat de la o abordare bazată pe frecvența cuvintelor către utilizarea modelelor de tip Transformer, specifice procesării limbajului natural moderne. Prin transformarea textului în vectori densi într-un spațiu semantic, modelul poate identifica relații de similitudine între concepte chiar și atunci când nu sunt folosite aceleași cuvinte cheie. Această abordare permite sistemului să propună etichete care reflectă esența semantică a lexei, reducând efortul manual al administratorului și crescând precizia categorisirii resurselor educaționale.

---

### Capitolul 3: Analiza de Business și Cerințe
#### 3.1. Contextul Pieței de M-Learning
Sistemele de învățare mobilă actuale se împart, în general, în trei categorii principale: LMS, aplicațiile de edutainment și platformele orientate către conținut. Din perspectiva arhitecturală, aceste soluții pot fi conceptualizate prin prisma modelului "Learning as a Service" (LaaS), propus de Butoi, Tomai și Mocean (2013) pentru instrumentele de învățare bazate pe cloud. Acest model permite scalabilitatea resurselor și eliminarea dependenței de dispozitivul final, transformând platforma într-un serviciu elastic de livrare a cunoșințelor.

**Sistemele LMS (ex. Moodle)** sunt optimizate pentru administrarea cursurilor și monitorizarea academică. Din perspectiva studentului, aceste platforme prezintă adesea o complexitate vizuală ridicată și un număr mare de interacțiuni necesare pentru a ajunge la conținutul efectiv al unei lecții. Interfețele sunt concepute primar pentru desktop, rezultând o experiență fragmentată pe dispozitivele portabile.

`[Screencapture: Comparație între ierarhia de navigare dintr-un curs Moodle vs. structura simplificată din Toolspaedeia]`

**Aplicațiile de edutainment (ex. Duolingo, Brilliant)** utilizează modele de gamificare agresivă pentru a crește retenția utilizatorilor. Deși interfețele sunt fluide, accentul cade pe mecanisme de recompensare (streaks, ligi, animații complexe) în detrimentul profunzimii conținutului. Din punct de vedere tehnic, aceste aplicații sunt resursifice, consumând memorie și baterie considerabile datorită procesării intense pe client.

`[Screencapture: Analiză vizuală a elementelor de distragere din interfața unei aplicații de edutainment]`

**Platformele orientate către conținut (ex. Khan Academy)** reprezintă cel mai apropiat model de Toolspaedeia, prioritizând accesul rapid la informație și structura clară a cursurilor. Toolspaedeia preia această abordare de navigare intuitivă, dar aduce un plus de performanță prin utilizarea unei arhitecturi minimaliste (lean) și a standardului Markdown, oferind creatorilor de cursuri o flexibilitate mai mare în redactarea materialelor.

Toolspaedeia se poziționează ca un mediu de învățare fără distrageri (distraction-free), eliminând zgomotul vizual pentru a prioritiza concentrarea cognitivă asupra materialului studiat.

#### 3.2. Analiza Nevoilor Utilizatorilor
Pentru a defini funcționalitățile sistemului, s-au analizat două profiluri principale de utilizatori.

În cazul studentului, s-a identificat nevoia de a accesa informația în mod asincron. Dincolo de deplasările zilnice, a fost analizată și problema accesibilității geografice, definită ca posibilitatea ca un utilizator să descarce modulul de curs într-un punct cu conexiune stabilă, pentru a putea studia ulterior în zone unde accesul la internet este limitat sau inexistent. Cerințele principale includ reducerea numărului de click-uri până la conținut, asigurarea independenței de rețea prin suport offline și eficientizarea utilizării resurselor hardware.

Pentru publicatori, bariera principală identificată a fost timpul investit în formatarea conținutului. Nevoile principale au fost simplificarea redactării printr-un format standard care nu necesită cunoștințe de programare, reducerea efortului de categorisire prin sugestii automate de etichete și implementarea unui sistem de monetizare direct, fără complexitatea administrativă a unui magazin online.

#### 3.3. Modelul Economic și Obiectivele Proiectului
Spre deosebire de tendința actuală de a trece la modele de abonament recurent, fenomen cunoscut sub numele de oboseală a abonamentelor software (SaaS subscription fatigue), Toolspaedeia adoptă un model de **achiziție unică**.

Acest model a fost ales deoarece conținutul educațional static nu necesită mentenanță continuă a accesului după achiziție. Odată cumpărat, cursul devine proprietatea utilizatorului, oferindu-i stabilitate și control asupra resurselor sale. Această decizie nu are doar un fundament economic, ci și unul social; prin reducerea barierelor financiare de acces la educație, platforma se aliniază cu viziunea conform căreia tehnologiile informației și comunicării pot servi ca instrumente de reducere a sărăciei și de democratizarea accesului la cunoaștere (Urean, Lacatus și Mocean, 2016).

**Obiectivele funcționale și non-funcționale:**
Din punct de vedere funcțional, sistemul trebuie să asigure randarea corectă a formatului Markdown și a formulelor matematice, implementarea unui flux de plată securizat via Stripe și gestionarea progresiei utilizatorului prin marcarea modulelor.

Din perspectiva non-funcțională, prioritățile sunt timpul de răspuns minim prin utilizarea SSR și HTMX, accesibilitatea prin suport PWA pentru instalare pe ecranul principal și acces offline, precum și portabilitatea datelor prin utilizarea standardelor deschise pentru a preveni dependența de furnizor (vendor lock-in).

`[TABEL: Matrice de cerințe - Cerința $\rightarrow$ Soluția Tehnică $\rightarrow$ Obiectivul Atingerea]`

---

### Capitolul 4: Proiectarea Sistemului
#### 4.1. Proiectarea Arhitecturală
Sistemul este proiectat pe baza modelului MVT (Model-View-Template), o variantă a arhitecturii MVC, adaptată pentru a maximiza eficiența randării pe server și a reduce complexitatea client-side.

**Stratul de Model (Model)**
Reprezintă logica de business și interfața cu baza de date. Acesta gestionează validarea datelor, relațiile dintre entități și interogările necesare pentru extragerea conținutului. Într-o abordare "lean", modelele sunt proiectate pentru a fi atomice, evitând redundanța datelor și optimizând timpul de răspuns al interogărilor.

**Stratul de Vizualizare (View)**
Acționează ca controller, procesând cererile HTTP și interacționând cu modelele pentru a prelua datele necesare. În cazul Toolspaedeia, stratul de vizualizare implementează logica de decizie pentru a determina dacă trebuie să returneze o pagină întreagă (pentru prima încărcare) sau doar un fragment de HTML (pentru cererile HTMX), optimizând astfel traficul de rețea.

**Stratul de Template (Template)**
Se ocupă de prezentarea finală a datelor. Template-urile sunt structurate modular, utilizând fragmente reutilizabile care pot fi randați independent. Această modularitate permite implementarea componentelor cu "auto-refresh", unde un fragment de interfață își definește propria logică de actualizare fără a necesita reîncărcarea întregii pagini.

`[DIAGRAMA: Arhitectura generală MVT adaptată pentru Toolspaedeia]`

#### 4.2. Proiectarea Bazei de Date
Baza de date a fost proiectată pentru a asigura integritatea referențială și performanța accesării conținutului, utilizând un model relațional.

Sistemul utilizează o strategie hibridă de stocare a datelor pentru a optimiza ciclul de dezvoltare și performanța în producție. În mediul de dezvoltare local, s-a optat pentru **SQLite3**, datorită simplității configurării și vitezei de iterație. În mediul de producție (PythonAnywhere), sistemul utilizează **MySQL**, asigurând stabilitatea tranzacțiilor și o gestionare mai eficientă a concurenței pe server.

**Sistemul de Entități și Relații**
Sistemul este construit în jurul a patru entități principale:
- **Utilizatorii**: Gestionează datele de autentificare și preferințele de interfață.
- **Cursurile**: Reprezintă unitatea principală de organizare a conținutului, conținând metadate și setul de module asociate.
- **Modulele**: Reprezintă unitățile atomice de învățare, fiecare modul fiind asociat cu un fișier de conținut Markdown și un set de resurse suplimentare.
- **Achizițiile**: Gestionează relația de posesie între utilizator și curs, stocând starea plății și data accesării.

S-a implementat o constrângere de unicitate pe perechea (Utilizator, Curs) în tabelul achizițiilor pentru a preveni duplicatele și a asigura consistența tranzacțiilor.

`[DIAGRAMA: Diagrama ER (Entity-Relationship) a bazei de date]`

#### 4.3. Proiectarea Fluxurilor de Lucru (Workflows)
Pentru a asigura stabilitatea sistemului, procesele critice au fost proiectate ca fluxuri liniare cu puncte de validare clare.

**Fluxul de Achiziție și Acces la Conținut**
Procesul de achiziție este conceput pentru a minimiza fricțiunea utilizatorului:
1. Utilizatorul selectează un curs și este redirecționat către platforma de plată Stripe.
2. După finalizarea tranzacției, Stripe trimite un webhook către serverul Toolspaedeia.
3. Serverul validează semnătura webhook-ului și actualizează starea achiziției în baza de date.
4. Utilizatorul primește acces instantaneu la modulele cursului.

`[DIAGRAMA: Fluxul de procesare a unei plăți Stripe - Sequence Diagram]`

**Fluxul de Sugerare Automată a Etichetelor**
Pentru a optimiza administrarea, procesul de generare a tag-urilor utilizează un model de limbaj pre-antrenat pentru a extrage esența semantică a conținutului:
1. Extragerea textului brut din fișierul Markdown al modulului.
2. Generarea unei reprezentări vectoriale (embedding) a textului folosind modelul `paraphrase-MiniLM-L3-v2`.
3. Compararea vectorului de text cu un set de etichete predefinite sau extragerea termenilor cu cea mai mare densitate semantică.
4. Propunerea celor mai relevante etichete către administrator.

`[DIAGRAMA: Fluxul de procesare a textului pentru generarea de tag-uri]`

**Fluxul de Navigare și Descoperire a Conținutului**
Pentru a reduce sarcina cognitivă a utilizatorului, interfața a fost proiectată pentru a minimiza reîncărcările complete ale paginii. S-a implementat o funcționalitate de "infinite scroll" pentru listele de cursuri, utilizând HTMX pentru a încărca pagini suplimentare de rezultate în mod asincron, oferind o experiență de navigare fluidă.

Sistemul de căutare a fost extins pentru a permite filtrarea cursurilor bazată pe etichete (tags). Utilizatorul poate interoga baza de date folosind termeni specifici, iar sistemul returnează cursurile care prezintă cea mai mare relevanță semantică sau potrivire exactă a tag-urilor, optimizând astfel procesul de descoperire a resurselor educaționale.

---

### Capitolul 5: Implementarea Sistemului
#### 5.1. Gestionarea Dependențelor și Calitatea Codului
Pentru a asigura stabilitatea sistemului și reproducibilitatea mediului de execuție, s-a renunțat la gestionarea tradițională a pachetelor în favoarea instrumentului `uv`. Această rigurozitate în gestionarea dependențelor este esențială deoarece, așa cum subliniază Thomas (2025), fiecare dependență externă introduce un grad de pierdere a controlului asupra propriei aplicații, transferând responsabilitatea stabilității către terți. Implementarea s-a bazat pe utilizarea unui fișier `pyproject.toml` pentru definirea dependențelor și a unui `uv.lock` pentru fixarea versiunilor exacte ale librăriilor. Această abordare elimină riscul de incompatibilitate între mediul de dezvoltare și cel de producție.

Sistematizarea calității codului a fost realizată prin integrarea `ruff` și `djlint` într-un flux de lucru automatizat via `pre-commit`. Această configurare forțează validarea sintactică și formatarea automată a codului Python și a template-urilor HTML înainte de orice commit în repository.

`[SNIPPET: Configurația .pre-commit-config.yaml pentru Ruff și djLint]`

#### 5.2. Implementarea Modulului de Plăți
Integrarea sistemului de plăți a fost realizată utilizând SDK-ul Stripe. Fluxul de implementare a fost împărțit în două componente: gestionarea sesiunii de checkout și procesarea confirmării plății.

Pentru a securiza procesul, s-a implementat un endpoint de webhook care primește notificările asincrone de la Stripe. Validarea plății nu se bazează pe răspunsul clientului, ci pe verificarea semnăturii digitale a webhook-ului Stripe, asigurând faptul că actualizarea stării de achiziție în baza de date are loc doar după confirmarea oficială a tranzacției.

`[SNIPPET: Implementarea funcției de validare a semnăturii Webhook-ului Stripe]`
`[SCREENSHOT: Interfața de checkout Stripe cu detaliile cursului]`

#### 5.3. Implementarea Capabilităților PWA
Transformarea platformei într-o Progressive Web App a presupus definirea unui fișier `manifest.json` pentru a permite instalarea aplicației pe ecranul principal al dispozitivului mobil, oferind o experiență similară cu cea a unei aplicații native.

Nucleul funcționalității offline este Service Worker-ul, implementat pentru a intercepta cererile HTTP și a servi resurse din cache. S-a configurat o strategie de caching pentru fișierele statice (CSS, JS) și pentru paginile critice, asigurând că utilizatorul poate naviga prin modulele deja descărcate chiar și în absența unei conexiuni la internet.

`[SNIPPET: Configurația Service Worker pentru caching-ul resurselor statice]`
`[SCREENSHOT: Prompt-ul de instalare PWA pe un dispozitiv Android/iOS]`

#### 5.4. Implementarea Sistemului de Sugestii cu Sentence-Transformers
Sistemul de sugestii automate pentru etichete a fost implementat ca un serviciu de analiză a textului integrat în panoul de administrare. Pentru a depăși limitările analizelor statistice simple, s-a utilizat biblioteca `sentence-transformers` din ecosistemul PyTorch.

Procesul de implementare a urmat un pipeline de Deep Learning:
1. **Sarcina de Embedding**: Utilizarea modelului pre-antrenat `paraphrase-MiniLM-L3-v2` pentru a converti textul lecsiilor în vectori de dimensiune fixă, care capturează contextul semantic.
2. **Calculul Similitudinii**: Implementarea unei funcții de similitudine cosinus pentru a măsura distanța dintre vectorul textului modulului și vectorii reprezentativi ai etichetelor disponibile.
3. **Filtrarea și Clasificarea**: Selecția celor mai relevante etichete bazată pe praguri de încredere semantice.

Această implementare permite sistemului să sugereze tag-uri relevante chiar dacă cuvintele exacte nu apar în text, oferind o categorisire mult mai inteligentă a resurselor.

`[SNIPPET: Implementarea funcției de embedding folosind SentenceTransformer]`
`[SCREENSHOT: Interfața de administrare a cursurilor cu sugestiile de tag-uri]`

#### 5.5. Deployment și Operarea în Medii de Producție
Platforma a fost deplasată pe serviciul PythonAnywhere, utilizând un server WSGI pentru gestionarea cererilor. Pentru a asigura securitatea și performanța, s-a implementat un fișier de setări separat (`settings_pythonanywhere.py`), care suprascrie variabilele de mediu critice.

O decizie critică în faza de deployment a fost migrarea bazei de date de la SQLite3 la MySQL. Deși SQLite3 a fost utilizat în faza de dezvoltare locală pentru a maximiza viteza de iterație, mediul de producție a necesitat un sistem de management al bazei de date (DBMS) mai robust, capabil să gestioneze concurența cererilor HTTP și să asigure integritatea datelor la scară mai largă.

Procesul de deployment a fost automatizat printr-un script care efectuează sincronizarea dependențelor prin `uv`, rulează migrarea bazei de date și colectează fișierele statice.

`[SNIPPET: Fragment din settings_pythonanywhere.py pentru configurarea securității]`
`[SCREENSHOT: Consola de administrare PythonAnywhere cu statusul aplicației]`

---

### Capitolul 6: Evaluarea și Validarea Calității

Acest capitol prezintă metodologia de testare utilizată pentru a asigura stabilitatea sistemului și analiza metricilor de performanță, validând astfel atingerea obiectivelor propuse la începutul lucrării.

#### 6.1. Strategia de Testare de Integrare
Spre deosebire de testarea unitară, care validează funcții izolate, s-a implementat o strategie de testare de integrare pentru a verifica corectitudinea fluxurilor complete de lucru. S-a utilizat instrumentul `webtest` pentru a simula interacțiunile utilizatorului cu serverul, alegând această soluție pentru a evita overhead-ul resurselor necesar rulării unor browsere reale (precum în cazul Selenium).

Testele au fost concentrate pe cele trei procese critice ale aplicației: autentificarea utilizatorilor, fluxul de achiziție a cursurilor și randarea corectă a conținutului Markdown. Validarea a presupus simularea unor scenarii de eroare, cum ar fi încercarea de acces la un modul neachiziționat sau trimiterea de date invalide către endpoint-urile de plată, asigurând astfel robustețea sistemului în fața input-urilor incorecte.

`[TABEL: Lista testelor de integrare executate și rezultatul acestora]`

#### 6.2. Analiza Acoperirii Codului (Code Coverage)
Pentru a cuantifica gradul de validare a logicii de backend, s-a utilizat instrumentul `coverage`. Această analiză a permis identificarea zonilor de cod care nu au fost executate în timpul testelor de integrare, oferind o imagine obiectivă asupra stabilității sistemului.

S-a observat o acoperire ridicată în ceea ce privește logica de randare și procesarea plăților, zonele critice ale aplicației. În schimb, unele ramuri de erori rare în procesul de deployment au prezentat o acoperire mai scăzută, ceea ce a condus la rafinarea seturilor de date utilizate în testele de simulare.

`[TABEL: Procentul de acoperire a codului pe module (Courses, Users, Purchases)]`

#### 6.3. Evaluarea Performanței și a Funcționalităților
Validarea performanței a fost realizată prin măsurarea unor indicatori cheie, comparând abordarea "lean" cu cea a platformelor educaționale convenționale.

Din perspectiva consumului de memorie, s-a observat că utilizarea unei arhitecturi bazate pe SSR (Server-Side Rendering) și HTMX reduce drastic amprenta de memorie pe dispozitivul mobil, deoarece majoritatea procesării are loc pe server. Timpul de primă pictare (First Contentful Paint) a fost optimizat prin minimizarea payload-ului CSS, rezultând o încărcare aproape instantanee a paginilor de curs.

În ceea de ceea ce privește performanța bazei de date, s-a efectuat o analiză comparativă între trei soluții de stocare: SQLite, MySQL și serviciul Neon (PostgreSQL).

S-a observat că utilizarea serviciului Neon a introdus o latență semnificativă, cu timpi de răspuns depășind adesea 600 ms. Această degradare a performanței a fost atribuită overhead-ului de conexiune și timpului de propagare a pachetelor (Round Trip Time - RTT) între serverul de aplicații și serverul de bază de date extern. În contrast, migrarea către MySQL găzduit pe aceeași infrastructură cu aplicația (PythonAnywhere) a redus latența la aproximativ 150 ms. Această optimizare a confirmat importanța proximității fizice a bazei de date față de serverul de execuție pentru a minimiza latențele de rețea în aplicațiile web.

S-a validat în plus funcționalitatea PWA prin simularea unei întreruperi a conexiunii la internet. Sistemul a reușit să servească paginile de curs din cache-ul local, confirmând că utilizatorul poate continua studiul fără întreruperi, validând astfel obiectivul de accesibilitate geografică.

`[TABEL: Metricile de performanță: Timp de răspuns, Consum Memorie, Acuratețe ML]`

#### 6.4. Analiza Critică și Limitări
Deși obiectivele principale au fost atinse, sistemul prezintă anumite limitări. Modelul de sugestii automate pentru etichete utilizează o abordare statistică simplă, care ar putea deveni insuficientă pe măsur la ce volumul de date crește, necesitând eventual trecerea la un model de limbaj mai complex.

De asemenea, dependența de un singur furnizor de găzduire (PythonAnywhere) reprezintă un punct de vulnerabilitate în ceea ce privește scalabilitatea extremă. Cu toate acestea, pentru talia actuală a proiectului, această soluție oferă cel mai bun raport cost-eficiență și simplitate de mentenanță.

`[Screencapture: Raportul final generat de instrumentul de coverage]

---

## 7. Concluzii
- Recapitularea obiectivelor atinse în cadrul proiectului.
- Analiza critică a soluției implementate: impactul abordării "lean" asupra experienței utilizatorului.
- **Reflecție personală:** Descrierea competențelor dobândite pe parcursul lucrării (stăpânirea framework-ului Django, implementarea PWA, utilizarea instrumentelor de analiză statică precum Ruff și gestionarea pachetelor cu uv).
- **Contribuția principală:** Crearea unei platforme educaționale care demonstrează că minimalismul tehnologic poate conduce la o experiență de învățare superioară.
- Direcții de extindere a proiectului (ex: implementarea unui sistem de feedback, extinderea modelului de ML).

---

## 8. Bibliografie
1. **Bologa, C., Buchmann, R. A., Sitar-Tăut, D. A.** (2024). *Ghid de elaborare a lucrării de licență la programul de studii Informatică Economică*. ASE.
2. **Butoi, Tomai, Mocean L.**. *Analiza impactului tehnologiilor informaționale asupra proceselor educaționale*. Revista IE, ASE. [https://www.revistaie.ase.ro/content/66/03%20-%20Butoi,%20Tomai,%20Mocean.pdf]
3. **Fielding, R. T.** (2000). *Architectural Styles with First-Class Constraints: REST for the World Wide Web*. University of California, Irvine.
4. **HTMX Documentation**. *Hypermedia for HTML*. [https://htmx.org/docs/]
5. **Hugging Face**. *Sentence-transformers/paraphrase-MiniLM-L3-v2 Model Card*. [https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2]
6. **Pico CSS Documentation**. *A Minimalist CSS Framework*. [https://picocss.com/docs]
7. **Poppendieck, M., Poppendieck, T.** (2003). *Lean Software Development: From Domain Driven Design to Agile*. Addison-Wesley Professional.
8. **Scikit-learn Developers**. *User Guide: Supervised Learning and Text Classification*. [https://scikit-learn.org/stable/user_guide.html]
9. **Stripe Inc**. *Stripe API Reference and Webhook Integration Guide*. [https://stripe.com/docs/api]
10. **Thomas, D.**. *Simplicity: The Art of Reducing Complexity in Software Systems*. O'Reilly Media, Inc.
11. **Urean, C. A., Lacatus, V. D., Mocean, L.** (2016). *Information And Communications Technology As A Poverty Reduction Tool*. Annals - Economy Series, Constantin Brancusi University.
12. **Volkmann, R. M.**. *Server Driven Web Apps with htmx*. O'Reilly Media, Inc.

---

## 9. Glosar de termeni
- **HATEOAS:** (Hypermedia as the Engine of Application State) Un constraint de arhitectură REST unde clientul interacționează cu serverul exclusiv prin hypermedia.
- **Service Worker:** Un script care rulează în fundal, separat de pagina web, permițând funcționalități precum caching și notificări push.
- **Linter:** Un instrument de analiză statică care verifică codul sursă pentru erori programate, bug-uri sau stil de programare non-conform.
- **WSGI:** (Web Server Gateway Interface) Un standard de comunicare între serverele web și aplicațiile Python.

---

## 10. Anexe
- [Screencapture: Interfața de administrare a cursurilor]
- [Screencapture: Interfața utilizatorului final (Desktop și Mobile)]
