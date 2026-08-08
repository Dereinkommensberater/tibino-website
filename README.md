# tibinokids.com

Statische Website für die Kinderserie **Tibino Kids**. Keine Build-Kette, kein Framework — HTML,
CSS und Bilder. Kann direkt bei Cloudflare Pages oder GitHub Pages liegen.

```
index.html        Startseite
privacy.html      Datenschutz
css/style.css     gesamtes Design (mobile first)
css/fonts.css     selbst gehostete Schriften
css/fonts/        Fredoka + Nunito als woff2
img/              Logo, Hero, Figuren-Freisteller, Folgen-Thumbnails, Favicon
robots.txt        erlaubt Suchmaschinen UND KI-Crawler
llms.txt          Kurzfassung für KI-Assistenten
sitemap.xml       zwei Seiten
```

## Noch offen

| Was | Wo | Status |
|---|---|---|
| **YouTube-Handle** | 9 Stellen in `index.html`, `privacy.html`, `llms.txt` | steht auf `@TibinoKids` — ungeprüft, per Suchen & Ersetzen tauschen |
| **Video ist privat** | YouTube Studio | Das eingebettete Video `4lVsG8rb3iI` ist auf „privat" gesetzt. Erst wenn es auf **öffentlich** oder **nicht gelistet** steht, lässt es sich abspielen. |
| **Kontakt-E-Mail** | `privacy.html` | `hello@tibinokids.com` — anpassen, falls eine andere Adresse gilt |

Der Abo-Link nutzt überall `?sub_confirmation=1` — YouTube öffnet damit sofort den
Abonnieren-Dialog statt nur die Kanalseite.

## Veröffentlichen

**Cloudflare Pages** (empfohlen, arbeitet auch mit einem privaten Repository):
Pages → Create → Connect to Git → dieses Repo → Framework preset `None`, Build command leer,
Output directory `/`. Danach unter Custom domains `tibinokids.com` und `www.tibinokids.com`
hinzufügen.

**GitHub Pages** läuft bereits: https://dereinkommensberater.github.io/tibino-website/

## Warum die Seite so gebaut ist

- **Kein Formular, kein Tracking, keine Cookies.** Die Zielgruppe sind Kinder unter 13; unter COPPA
  löst schon eine Newsletter-Anmeldung Einwilligungspflichten aus. Der einfachste sichere Weg ist,
  gar nichts zu erheben. Der Abo-Weg läuft komplett über YouTube.
- **Das Video lädt erst beim Klick.** Vorher geht keine einzige Anfrage an YouTube — besser für den
  Datenschutz, schneller im Aufbau, und ein noch nicht öffentliches Video zeigt das Vorschaubild
  statt einer Fehlermeldung.
- **Schriften liegen auf dem eigenen Server.** Google Fonts würde die IP jedes Besuchers an Google
  melden; das ist bei einer Kinderseite der unnötigste Datenabfluss überhaupt.
- **Strukturierte Daten** (`Organization`, `WebSite`, `TVSeries` mit allen Figuren, `FAQPage`)
  liegen als JSON-LD in `index.html` — der Hebel dafür, dass ChatGPT, Perplexity und Google-KI die
  Serie korrekt wiedergeben, wenn Eltern nach sicheren Kindersendungen fragen.
- **`llms.txt`** fasst dieselben Fakten zitierfähig zusammen.
- **Figurengrößen sind gestaffelt.** Ohne das war Pip — die kleinste Figur der Serie — größer als
  Tibino, weil alle Freisteller auf derselben Bildhöhe lagen.
- **Mobile first.** Alle Breakpoints gehen nach oben (`min-width`), geprüft bei 375, 768 und
  1440 px auf horizontalen Überlauf, fehlende Bilder und Konsolenfehler.

## Prüfen nach einer Änderung

Die Seite muss über **HTTP** getestet werden, nicht per Doppelklick: Unter `file://` blockiert der
Browser die eigenen Schriftdateien, und man sieht Fehler, die es in Wirklichkeit nicht gibt.

```bash
python -m http.server 8749 --directory .
```
