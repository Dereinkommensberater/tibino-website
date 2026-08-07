# tibinokids.com

Statische Website für die Kinderserie **Tibino Kids**. Keine Build-Kette, kein Framework — HTML,
CSS und Bilder. Kann direkt bei Cloudflare Pages oder GitHub Pages liegen.

```
index.html        Startseite
privacy.html      Datenschutz
css/style.css     gesamtes Design (mobile first)
img/              Hero, Figuren-Freisteller, Folgen-Thumbnails, Favicon
robots.txt        erlaubt Suchmaschinen UND KI-Crawler
llms.txt          Kurzfassung für KI-Assistenten
sitemap.xml       zwei Seiten
```

## Vor dem Livegang: drei Stellen eintragen

| Was | Wo | Aktuell |
|---|---|---|
| **YouTube-Handle** | `index.html`, `privacy.html`, `llms.txt`, `robots.txt` | `@TibinoKids` — per Suchen & Ersetzen tauschen |
| **Video-ID der Vorstell-Folge** | `index.html`, Block `.video-embed` | `VIDEO_ID` |
| **Kontakt-E-Mail** | `privacy.html` | `hello@tibinokids.com` |

Der Abo-Link nutzt überall `?sub_confirmation=1` — YouTube öffnet damit sofort den
Abonnieren-Dialog, statt nur die Kanalseite zu zeigen.

Solange die Videos nicht online sind, zeigt der Einbettungsblock einen Fehler. Bis dahin entweder
die Video-ID eintragen oder den Block auskommentieren; die beiden Folgen-Karten darüber
funktionieren unabhängig davon.

## Veröffentlichen

**Cloudflare Pages** (empfohlen, arbeitet auch mit einem privaten Repository):
Pages → Create → Connect to Git → dieses Repo → Framework preset `None`, Build command leer,
Output directory `/`. Danach unter Custom domains `tibinokids.com` und `www.tibinokids.com`
hinzufügen.

**GitHub Pages** geht auch, verlangt bei einem kostenlosen Konto aber ein öffentliches Repository:
Settings → Pages → Branch `master`, Ordner `/`.

## Warum die Seite so gebaut ist

- **Kein Formular, kein Tracking, keine Cookies.** Die Zielgruppe sind Kinder unter 13; unter COPPA
  löst schon eine Newsletter-Anmeldung Einwilligungspflichten aus. Der einfachste sichere Weg ist,
  gar nichts zu erheben. Der Abo-Weg läuft komplett über YouTube.
- **Videos über `youtube-nocookie.com`.** YouTubes datenschutzfreundlicher Modus.
- **Strukturierte Daten** (`Organization`, `WebSite`, `TVSeries` mit allen Figuren, `FAQPage`)
  liegen als JSON-LD in `index.html`. Sie sind der Hebel dafür, dass ChatGPT, Perplexity und
  Google-KI die Serie korrekt wiedergeben, wenn Eltern nach sicheren Kindersendungen fragen.
- **`llms.txt`** fasst dieselben Fakten in einer Form zusammen, die Sprachmodelle direkt zitieren
  können — die Elternfragen stehen dort ausformuliert.
- **Mobile first.** Alle Breakpoints gehen nach oben (`min-width`), geprüft bei 375, 768 und
  1440 px auf horizontalen Überlauf.

## Offener Punkt

Die beiden Schriften kommen von Google Fonts, d. h. der Browser des Besuchers kontaktiert Google.
Für die DSGVO ist Selbsthosten sauberer: Fredoka und Nunito herunterladen, unter `css/fonts/`
ablegen, per `@font-face` einbinden und den Google-Link entfernen. Dann kann auch der
entsprechende Absatz aus `privacy.html` raus.
