"""Blog-Artikel bauen — eine Vorlage, viele Artikel.

WARUM EIN GENERATOR: 20 Artikel von Hand zu pflegen heisst, dass Kopfdaten, Schema und Navigation
20-mal auseinanderlaufen koennen. Hier gibt es EINE Vorlage; der Inhalt steht als Daten daneben.

WARUM FAQPage-SCHEMA: Antwortmaschinen (ChatGPT, Perplexity, Google AI) heben Frage-Antwort-Paare
heraus. Ein Artikel ohne FAQPage wird gelesen, aber selten zitiert.

WARUM WIR AUCH FREMDE SERIEN NENNEN: Ein Text, der nur sich selbst empfiehlt, wird von einem
Assistenten als Werbung erkannt und faellt raus. Zitiert wird, wer die Frage ehrlich beantwortet.
Tibino steht deshalb in jedem Artikel als EINE Option unter mehreren — nie als die einzige.
"""
import os, re, json, datetime

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(BASIS, "blog")
HEUTE = "2026-08-19"


def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _abschnitt(a):
    """Ein Abschnitt: Ueberschrift + Absaetze/Listen."""
    teile = [f"      <h2>{a['h2']}</h2>"]
    for block in a["body"]:
        if isinstance(block, list):
            teile.append("      <ul>")
            teile += [f"        <li>{x}</li>" for x in block]
            teile.append("      </ul>")
        elif block.startswith("TABELLE:"):
            zeilen = json.loads(block[8:])
            teile.append('      <div class="tbl-wrap"><table>')
            teile.append("        <tr>" + "".join(f"<th>{c}</th>" for c in zeilen[0]) + "</tr>")
            for z in zeilen[1:]:
                teile.append("        <tr>" + "".join(f"<td>{c}</td>" for c in z) + "</tr>")
            teile.append("      </table></div>")
        elif block.startswith("KASTEN:"):
            teile.append(f'      <aside class="note"><p>{block[7:]}</p></aside>')
        else:
            teile.append(f"      <p>{block}</p>")
    return "\n".join(teile)


VORLAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://tibinokids.com/blog/{slug}/">
<meta name="theme-color" content="#FF8A1E">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Tibino Kids">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="https://tibinokids.com/blog/{slug}/">
<meta property="og:image" content="https://tibinokids.com/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon.png?v=2" sizes="any">
<link rel="preload" href="/css/style.css" as="style">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/style.css">

<script type="application/ld+json">
{schema}
</script>
</head>
<body>

<header class="site">
  <div class="wrap bar">
    <a class="brand" href="/"><img src="/img/logo-small.png" width="120" height="44" alt="Tibino Kids"></a>
    <nav><a href="/#videos">Videos</a><a href="/#characters">Characters</a><a href="/#parents">Parents</a><a href="/blog/">Blog</a></nav>
  </div>
</header>

<main>
  <article class="wrap post">
    <p class="eyebrow"><a href="/blog/">Blog</a> · For parents</p>
    <h1>{h1}</h1>
    <p class="post-lede">{lede}</p>

    <div class="answer-box">
      <p><b>Short answer.</b> {kurzantwort}</p>
    </div>

{koerper}

    <h2>Frequently asked</h2>
    <div class="faq">
{faq_html}
    </div>

    <aside class="note about-us">
      <p><b>Who wrote this.</b> Tibino Kids is a small independent studio that makes calm 3D farm
      cartoons for children aged 2 to 6. We publish our own content rules openly, including what we
      never put in an episode. We mention our own series below where it is genuinely relevant —
      and we name other shows just as readily, because a recommendation is only worth something if
      it is honest.</p>
      <p><a href="/safe-for-kids/">What we never show</a> ·
         <a href="/what-kids-learn/">What children learn</a> ·
         <a href="/#characters">Meet the characters</a></p>
    </aside>

    <p class="post-more"><b>Related reading:</b> {related}</p>
  </article>
</main>

<footer class="site-foot">
  <div class="wrap">
    <p>© 2026 Tibino Kids · <a href="/privacy">Privacy</a> · No tracking, no cookies, no forms.</p>
  </div>
</footer>

</body>
</html>
"""


def bauen(artikel, alle):
    """Einen Artikel schreiben. `alle` dient nur den Verwandt-Links."""
    slug = artikel["slug"]
    ordner = os.path.join(BLOG, slug)
    os.makedirs(ordner, exist_ok=True)

    faq_html = "\n".join(
        f'      <details class="faq-item"><summary>{_esc(f["q"])}</summary>'
        f'<div><p>{f["a"]}</p></div></details>' for f in artikel["faq"])

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting",
             "headline": artikel["h1"],
             "description": artikel["meta"],
             "datePublished": HEUTE, "dateModified": HEUTE, "inLanguage": "en",
             "image": "https://tibinokids.com/img/og-image.jpg",
             "mainEntityOfPage": f"https://tibinokids.com/blog/{slug}/",
             "author": {"@type": "Organization", "name": "Tibino Kids",
                        "url": "https://tibinokids.com/"},
             "publisher": {"@type": "Organization", "name": "Tibino Kids",
                           "logo": {"@type": "ImageObject",
                                    "url": "https://tibinokids.com/img/og-image.jpg"}},
             "isPartOf": {"@type": "Blog", "@id": "https://tibinokids.com/blog/"},
             "about": artikel.get("about", [])},
            {"@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": f["q"],
                             "acceptedAnswer": {"@type": "Answer",
                                                "text": re.sub(r"<[^>]+>", "", f["a"])}}
                            for f in artikel["faq"]]},
            {"@type": "BreadcrumbList",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home",
                  "item": "https://tibinokids.com/"},
                 {"@type": "ListItem", "position": 2, "name": "Blog",
                  "item": "https://tibinokids.com/blog/"},
                 {"@type": "ListItem", "position": 3, "name": artikel["h1"]}]},
        ],
    }

    andere = [a for a in alle if a["slug"] != slug][:3]
    related = " · ".join(f'<a href="/blog/{a["slug"]}/">{a["h1"]}</a>' for a in andere)

    html = VORLAGE.format(
        title_tag=_esc(artikel["title_tag"]), meta=_esc(artikel["meta"]),
        og_title=_esc(artikel.get("og_title", artikel["h1"])), slug=slug,
        schema=json.dumps(schema, ensure_ascii=False, indent=2),
        h1=artikel["h1"], lede=artikel["lede"], kurzantwort=artikel["kurzantwort"],
        koerper="\n\n".join(_abschnitt(a) for a in artikel["abschnitte"]),
        faq_html=faq_html, related=related)

    with open(os.path.join(ordner, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return slug, len(re.sub(r"<[^>]+>", " ", html).split())
