"""Generates the AREX Mining static site (ES default, EN) from one content source.
Adding a language later: add its strings to NAV/UI and each page's dict, plus LANGS."""
import os, sys

OUT = sys.argv[1]
LANGS = ["es", "en", "zh", "pt"]     # future: "de"
LANG_LABEL = {"es": "ES", "en": "EN", "zh": "中文", "pt": "PT", "de": "DE"}
HTML_LANG = {"es": "es", "en": "en", "zh": "zh-Hans", "pt": "pt-BR"}

def href(slug, lang):
    return f"{slug}.html" if lang == "es" else f"{slug}-{lang}.html"

# ---------------------------------------------------------------- shared bits
CONTOUR = ('<svg class="contour-bg" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true" '
           'xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">'
           '<path d="M-40 640 C 90 430, 170 330, 380 296 C 560 266, 660 214, 780 120 C 890 34, 1010 6, 1240 -14"/>'
           '<path d="M-40 750 C 90 540, 170 440, 380 406 C 560 376, 660 324, 780 230 C 890 144, 1010 116, 1240 96"/>'
           '<path d="M-40 860 C 90 650, 170 550, 380 516 C 560 486, 660 434, 780 340 C 890 254, 1010 226, 1240 206"/>'
           '<path d="M-40 970 C 90 760, 170 660, 380 626 C 560 596, 660 544, 780 450 C 890 364, 1010 336, 1240 316"/>'
           '</svg>')

ARG_PATH = ("M 65.2 11.4 L 98.6 11.4 L 122.2 28.6 L 138.5 44.6 L 171.0 51.4 L 180.1 67.4 L 165.6 84.6 L 158.4 105.2 "
            "L 143.9 105.2 L 139.4 128.0 L 136.7 148.6 L 147.5 164.6 L 152.0 176.0 L 144.8 195.5 L 114.0 204.6 "
            "L 101.4 203.5 L 100.5 220.6 L 77.8 226.3 L 76.9 241.2 L 89.6 243.5 L 82.4 250.3 L 74.2 274.3 L 63.4 275.5 "
            "L 53.4 285.8 L 69.7 307.5 L 58.8 323.5 L 46.2 334.9 L 45.2 357.8 L 44.3 387.5 L 63.4 388.6 L 44.3 382.9 "
            "L 47.1 369.2 L 31.7 361.2 L 10.9 349.8 L 13.6 320.0 L 1.8 297.2 L 16.3 272.0 L 14.5 240.0 L 19.0 212.6 "
            "L 23.5 188.6 L 33.5 157.7 L 30.8 131.4 L 27.2 108.6 L 37.1 82.3 L 46.2 57.1 L 57.0 34.3 Z")

PINS = {
    "tc": (58.8, 72, "Tres Cruces", "Catamarca"),
    "sr": (44.5, 166, "San Romeleo", "Malargüe, Mendoza"),
}

def arg_map(pins, label):
    out = [f'<svg class="sa-map" viewBox="-8 0 250 400" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">',
           f'<path class="sa-land" d="{ARG_PATH}"/>']
    for key in pins:
        x, y, name, prov = PINS[key]
        out.append(f'<circle class="sa-ring" cx="{x}" cy="{y}" r="12"/><circle class="sa-pin" cx="{x}" cy="{y}" r="4.5"/>'
                   f'<line x1="{x+12}" y1="{y}" x2="100" y2="{y-14}" stroke="#fff" stroke-width="1.1"/>'
                   f'<text class="sa-label" x="104" y="{y-16}">{name}</text>'
                   f'<text class="sa-label" x="104" y="{y-2}" style="font-size:10px;opacity:.8">{prov}</text>')
    out.append('</svg>')
    return "".join(out)

CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

NAV = {
    "es": {"index": "Inicio", "about": "Nosotros", "services": "Servicios", "projects": "Proyectos",
           "people": "Nuestra gente", "lab": "Nuestro laboratorio", "esg": "Sustentabilidad", "news": "Novedades", "contact": "Contacto",
           "privacy": "Privacidad", "copper": "Cobre", "lithium": "Litio", "gold": "Oro", "silver": "Plata",
           "menu": "Menú", "about_us": "Quiénes somos"},
    "en": {"index": "Home", "about": "About", "services": "Services", "projects": "Projects",
           "people": "Our People", "lab": "Our Lab", "esg": "ESG", "news": "News", "contact": "Contact",
           "privacy": "Privacy", "copper": "Copper", "lithium": "Lithium", "gold": "Gold", "silver": "Silver",
           "menu": "Menu", "about_us": "Who we are"},
}
ABOUT_SLUGS = {"about", "services", "people"}
PROJECT_SLUGS = {"copper", "san-romeleo", "lithium", "tres-cruces", "gold", "silver"}

UI = {
    "es": {
        "entity": "AREX MINING S.A. · Argentina",
        "legal": ("© 2026 AREX Mining S.A. Todos los derechos reservados. Este sitio tiene fines exclusivamente informativos y no "
                  "constituye una oferta ni una solicitud de oferta de compra de valores, ni asesoramiento de inversión. Las "
                  "declaraciones sobre planes, recursos y desempeño futuros son prospectivas, se basan en las expectativas de la "
                  "dirección a la fecha de publicación y están sujetas a hechos y circunstancias fuera del control de la empresa. "
                  "Los resultados reales pueden diferir significativamente. San Romeleo se desarrolla para AREX Copper y el "
                  "Proyecto Tres Cruces para 3C Resources; cada proyecto pertenece a su respectivo titular."),
        "social": "Seguí a AREX Mining en LinkedIn",
        "map": "Mapa de Argentina con la ubicación de los proyectos San Romeleo, en Mendoza, y Tres Cruces, en Catamarca",
        "more": "Ver proyecto",
        "learn": "Más información",
    },
    "en": {
        "entity": "AREX MINING S.A. · Argentina",
        "legal": ("© 2026 AREX Mining S.A. All rights reserved. This website is for general information only and does not "
                  "constitute an offer or solicitation of an offer for the purchase of any securities, nor investment advice. "
                  "Statements regarding future plans, resources and performance are forward-looking, are based on management "
                  "expectations as at the date of publication, and are subject to events and circumstances beyond the control "
                  "of the company. Actual results may differ materially. San Romeleo is developed for AREX Copper and the Tres "
                  "Cruces Project for 3C Resources; each project belongs to its respective owner."),
        "social": "Follow AREX Mining on LinkedIn",
        "map": "Map of Argentina showing the San Romeleo project in Mendoza and the Tres Cruces project in Catamarca",
        "more": "View project",
        "learn": "Learn more",
    },
}

# Mandarin pages reuse the English page structure; text is swapped from zh.json
for _l in ("zh", "pt"):
    NAV[_l] = dict(NAV["en"]); UI[_l] = dict(UI["en"])

import json, re as _re
HERE = os.path.dirname(os.path.abspath(__file__))
ZH_PATH = os.path.join(HERE, "zh.json")
TABLES = {l: (json.load(open(os.path.join(HERE, f"{l}.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, f"{l}.json")) else {}) for l in ("zh", "pt")}
ZH = TABLES["zh"]
CUR = {"t": ZH, "lang": "zh"}
MISSING = {}
KEEP = {"AREX Mining", "San Romeleo", "Tres Cruces", "ES", "EN", "中文", "PT", "→", "·", "*", "LinkedIn", "website"}

def _tr(text):
    t = text.strip()
    if not t or not _re.search(r"[A-Za-z]", t) or t in KEEP:
        return text
    tbl = CUR["t"]
    if t in tbl:
        return text.replace(t, tbl[t])
    MISSING.setdefault(CUR["lang"], set()).add(t)
    return text

def to_lang(html, lang):
    CUR["t"] = TABLES[lang]; CUR["lang"] = lang
    head, sep, rest = html.partition("<body>")
    def attr(m):
        return f'{m.group(1)}="{_tr(m.group(2))}"'
    head = _re.sub(r'<title>([^<]*)</title>', lambda m: f"<title>{_tr(m.group(1))}</title>", head)
    head = _re.sub(r'(content)="([^"]*)"', lambda m: attr(m) if 'name="viewport"' not in m.string[max(0,m.start()-40):m.start()] else m.group(0), head)
    rest = _re.sub(r'(alt|aria-label|value)="([^"]*)"', attr, rest)
    rest = _re.sub(r">([^<]+)<", lambda m: ">" + _tr(m.group(1)) + "<", rest)
    return head + sep + rest

def header(lang, slug):
    n = NAV[lang]
    def item(s):
        cur = ' aria-current="page"' if s == slug else ""
        return f'<li><a href="{href(s, lang)}"{cur}>{n[s]}</a></li>'
    def sub(s, child=False):
        cur = ' aria-current="page"' if s == slug else ""
        label = {"san-romeleo": "San Romeleo", "tres-cruces": "Tres Cruces"}.get(s) or n[s]
        cls = ' class="sub-child"' if child else ""
        return f'<li{cls}><a href="{href(s, lang)}"{cur}>{label}</a></li>'
    def dropdown(key, slugs_set, items):
        cur = " current" if slug in slugs_set else ""
        return (f'<li class="has-sub{cur}"><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-{key}" '
                f'onclick="const p=this.parentElement;const o=p.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)">'
                f'{n[key]}{CHEV}</button><ul class="sub" id="sub-{key}">{items}</ul></li>')
    about_link = (f'<li><a href="{href("about", lang)}"{" aria-current=\"page\"" if slug == "about" else ""}>{n["about_us"]}</a></li>')
    about = dropdown("about", ABOUT_SLUGS, about_link + sub("services") + sub("people"))
    projects = dropdown("projects", PROJECT_SLUGS,
                        sub("copper") + sub("san-romeleo", True) + sub("lithium") + sub("tres-cruces", True) + sub("gold") + sub("silver"))
    langs = "".join(
        f'<a href="{href(slug, l)}" hreflang="{HTML_LANG[l]}"{" aria-current=\"true\"" if l == lang else ""}>{LANG_LABEL[l]}</a>'
        for l in LANGS)
    return (f'<header class="site-header"><div class="wrap nav-bar">'
            f'<a class="brand" href="{href("index", lang)}"><img src="logo.svg" alt="AREX Mining" width="230" height="63"></a>'
            f'<button class="nav-toggle" aria-expanded="false" aria-controls="nav" '
            f'onclick="const n=document.getElementById(\'nav\');const o=n.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',o)">{n["menu"]}</button>'
            f'<ul class="nav-links" id="nav">{item("index")}{about}{projects}{item("lab")}'
            f'{item("esg")}{item("news")}{item("contact")}<li class="lang">{langs}</li></ul>'
            f'</div></header>')

LINKEDIN = ('<a href="https://www.linkedin.com/company/arexmining" target="_blank" rel="noopener" aria-label="LinkedIn">'
            '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM2 9h6v13H2zM10 9h5.7v1.8h.1c.8-1.3 2.4-2.2 4.3-2.2 3.9 0 4.9 2.3 4.9 5.9V22h-6v-6.2c0-1.5-.5-2.6-1.9-2.6-1.2 0-1.9.8-2.2 1.6-.1.3-.1.7-.1 1.1V22h-6V9z"/></svg></a>')

def footer(lang):
    n, u = NAV[lang], UI[lang]
    links = "".join(f'<a href="{href(s, lang)}">{n[s]}</a>' for s in
                    ["index", "about", "services", "people", "lab", "esg", "news", "contact", "privacy"])
    return (f'<footer class="site-footer"><div class="wrap">'
            f'<div class="cols"><a class="brand" href="{href("index", lang)}"><img src="logo-white.svg" alt="AREX Mining" width="200" height="55"></a>'
            f'<div class="social" aria-label="{u["social"]}">{LINKEDIN}</div></div>'
            f'<div class="cols" style="margin-bottom:1.6rem"><nav aria-label="Footer">{links}</nav></div>'
            f'<p class="entity">{u["entity"]}</p><p class="legal">{u["legal"]}</p></div></footer>')

def page(lang, slug, title, desc, body):
    alts = "".join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{href(slug, l)}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{href(slug, "es")}">'
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon-512.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="AREX Mining">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Archivo+Black&family=Archivo+Narrow:wght@700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
{alts}
<link rel="stylesheet" href="styles.css">
</head>
<body>
{header(lang, slug)}
<main>
{body}
</main>
{footer(lang)}
</body>
</html>
"""

def page_hero(eyebrow, h1, p=None, tall=False, img=None, alt=""):
    ptag = f"<p>{p}</p>" if p else ""
    cls = "page-hero tall" if tall else "page-hero"
    if img:
        return (f'<div class="{cls} photo"><img src="{img}" alt="{alt}" fetchpriority="high">'
                f'<div class="wrap"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>{ptag}</div></div>')
    return f'<div class="{cls}">{CONTOUR}<div class="wrap"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>{ptag}</div></div>'

def project_card(lang, slug, kicker, title, text):
    return (f'<a class="card" href="{href(slug, lang)}"><span class="kicker">{kicker}</span><h3>{title}</h3>'
            f'<p>{text}</p><span class="more">{UI[lang]["more"]} →</span></a>')

# ---------------------------------------------------------------- copy
MVV = {
    "es": [("Misión", "Generar proyectos mineros en armonía con el ambiente, respetando a las comunidades locales y contribuyendo efectivamente al desarrollo del país."),
           ("Visión", "Ser reconocidos como un desarrollador responsable de proyectos mineros."),
           ("Valores", "Transparencia, honestidad y confianza son nuestros ejes éticos en las negociaciones. La integridad define nuestro espíritu, actuando con responsabilidad y compromiso. Creemos en resultados sostenibles y prácticas de mejora continua.")],
    "en": [("Mission", "To develop mining projects in harmony with the environment, respecting local communities and contributing meaningfully to the country's development."),
           ("Vision", "To be recognised as a responsible developer of mining projects."),
           ("Values", "Transparency, honesty and trust are the ethical foundations of how we negotiate. Integrity defines our spirit, and we act with responsibility and commitment. We believe in sustainable results and continuous improvement.")],
}

MVV["zh"] = MVV["pt"] = MVV["en"]

def values_block(lang, dark=False):
    return '<div class="values">' + "".join(
        f'<div class="value"><h3>{h}</h3><p>{p}</p></div>' for h, p in MVV[lang]) + '</div>'

SERVICES = {
    "es": [
        ("Exploración y geología", "Mapeo geológico de superficie, muestreo, geofísica, perforación diamantina e hidrogeología para identificar y definir recursos minerales."),
        ("Estudios e ingeniería", "Gestión de estudios de alcance, prefactibilidad y factibilidad, y coordinación de ingeniería con consultoras especializadas."),
        ("Procesamiento y tecnología", "Ensayos de laboratorio, pruebas piloto y desarrollo de procesos para definir la ruta de procesamiento de cada yacimiento."),
        ("Permisos y aprobaciones", "Informes de impacto ambiental, permisos de agua y gestión ante las autoridades mineras y ambientales provinciales."),
        ("Comunidad y ambiente", "Relaciones comunitarias, monitoreo ambiental y programas de gestión social desde las primeras etapas del proyecto."),
        ("Construcción y puesta en marcha", "Logística, gestión de la construcción, puesta en marcha y transición a la etapa de producción."),
    ],
    "en": [
        ("Exploration and geology", "Surface geological mapping, sampling, geophysics, diamond drilling and hydrogeology to identify and define mineral resources."),
        ("Studies and engineering", "Management of scoping, pre-feasibility and feasibility studies, and coordination of engineering with specialist consultancies."),
        ("Processing and technology", "Laboratory testwork, piloting and process development to define the processing route for each deposit."),
        ("Permitting and approvals", "Environmental impact assessments, water permits and engagement with provincial mining and environmental authorities."),
        ("Community and environment", "Community relations, environmental monitoring and social management programs from the earliest project stages."),
        ("Construction and commissioning", "Logistics, construction management, commissioning and the transition into production."),
    ],
}

SERVICES["zh"] = SERVICES["pt"] = SERVICES["en"]

def services_grid(lang, n=6):
    return '<div class="grid grid-3" style="margin-top:2.4rem">' + "".join(
        f'<div class="card"><h3>{h}</h3><p>{p}</p></div>' for h, p in SERVICES[lang][:n]) + '</div>'

# ---------------------------------------------------------------- pages
PAGES = {}

def home(lang):
    if lang == "es":
        hero = ('<div class="hero">' + CONTOUR + '<div class="wrap"><span class="eyebrow">Mendoza · Catamarca · Argentina</span>'
                '<p class="hero-title">Exploración de minerales y desarrollo de proyectos mineros</p>'
                '<p class="hero-sub">Transformamos desafíos en oportunidades, comprometidos con la sustentabilidad y con las comunidades locales.</p>'
                f'<a class="btn btn-ghost" href="{href("services", lang)}">Nuestros servicios</a></div></div>')
        strip = [("Equipo integral", "de la exploración a la producción"), ("Raíces en Argentina", "experiencia global, conocimiento local"),
                 ("Cartera multimineral", "diversos minerales en desarrollo"), ("Trayectoria probada", "Cauchari y Tres Quebradas (3Q)")]
        intro = ('<span class="eyebrow">Bienvenidos a AREX Mining</span>'
                 '<h2>Quiénes somos</h2>'
                 '<p>AREX Mining es una empresa argentina de servicios mineros. Contamos con un equipo altamente capacitado que se destaca por su dedicación e integridad, y que aporta experiencia internacional y conocimiento local a cada proyecto. Nuestro compromiso con la innovación y la investigación nos permite ser pioneros en la industria.</p>'
                 '<h2 style="margin-top:2.2rem">Qué hacemos</h2>'
                 '<p>Exploramos minerales y desarrollamos proyectos mineros para sus titulares, desde el descubrimiento hasta la producción. Gestionamos cada etapa: exploración, estudios e ingeniería, permisos, relación con las comunidades y construcción, manteniendo nuestro compromiso con la sustentabilidad y la responsabilidad ambiental.</p>')
        proj_h = ('Proyectos', 'Los proyectos que desarrollamos')
        cards = (project_card(lang, "san-romeleo", "Cobre · Malargüe, Mendoza", "San Romeleo",
                              "Reactivación productiva de un cuerpo de cobre oxidado y exploración del distrito, desarrollado para AREX Copper.") +
                 project_card(lang, "tres-cruces", "Litio · Catamarca", "Proyecto Tres Cruces",
                              "Depósito de salmuera de litio de grado batería en la Puna catamarqueña, desarrollado para 3C Resources."))
        svc_h = ('Servicios', 'Un solo equipo, de la exploración a la producción',
                 'Reunimos todas las disciplinas necesarias para llevar un proyecto desde el descubrimiento hasta la operación.')
        vals_h = ('Lo que nos guía', 'Misión, visión y valores')
        all_svc = "Ver todos los servicios"
    else:
        hero = ('<div class="hero">' + CONTOUR + '<div class="wrap"><span class="eyebrow">Mendoza · Catamarca · Argentina</span>'
                '<p class="hero-title">Mineral exploration and mining project development</p>'
                '<p class="hero-sub">Turning challenges into opportunities, committed to sustainability and to local communities.</p>'
                f'<a class="btn btn-ghost" href="{href("services", lang)}">Our services</a></div></div>')
        strip = [("One team", "from exploration to production"), ("Rooted in Argentina", "international experience, local expertise"),
                 ("Multi-mineral portfolio", "a range of minerals in development"), ("Proven track record", "Cauchari and Tres Quebradas (3Q)")]
        intro = ('<span class="eyebrow">Welcome to AREX Mining</span>'
                 '<h2>Who we are</h2>'
                 '<p>AREX Mining is an Argentine mining services company. Our highly skilled team stands out for its dedication and integrity, bringing international experience and local expertise to every project. Our commitment to innovation and research allows us to break new ground in the industry.</p>'
                 '<h2 style="margin-top:2.2rem">What we do</h2>'
                 '<p>We explore for minerals and develop mining projects for their owners, from discovery through to production. We manage every stage, from exploration, studies and engineering to permitting, community relations and construction, whilst remaining committed to sustainability and environmental responsibility.</p>')
        proj_h = ('Projects', 'The projects we develop')
        cards = (project_card(lang, "san-romeleo", "Copper · Malargüe, Mendoza", "San Romeleo",
                              "Productive reactivation of an oxidised copper body and exploration of the surrounding district, developed for AREX Copper.") +
                 project_card(lang, "tres-cruces", "Lithium · Catamarca", "The Tres Cruces Project",
                              "A battery-grade lithium brine deposit on the Catamarca Puna, developed for 3C Resources."))
        svc_h = ('Services', 'One team, from exploration to production',
                 'We bring together every discipline needed to take a project from discovery to operation.')
        vals_h = ('What guides us', 'Mission, vision and values')
        all_svc = "View all services"
    strip_html = '<div class="strip"><div class="wrap">' + "".join(
        f'<div class="cell"><b>{b}</b><span>{s}</span></div>' for b, s in strip) + '</div></div>'
    body = (hero + strip_html +
            f'<section class="section-deep"><div class="wrap map-panel">{arg_map(["tc", "sr"], UI[lang]["map"])}<div>{intro}</div></div></section>'
            f'<section><div class="wrap"><span class="eyebrow">{proj_h[0]}</span><h2>{proj_h[1]}</h2>'
            f'<div class="grid grid-2" style="margin-top:2.2rem">{cards}</div></div></section>'
            f'<section class="section-alt"><div class="wrap"><span class="eyebrow">{svc_h[0]}</span><h2>{svc_h[1]}</h2>'
            f'<p class="lede">{svc_h[2]}</p>{services_grid(lang, 3)}'
            f'<p style="margin-top:2.2rem"><a class="btn" href="{href("services", lang)}">{all_svc}</a></p></div></section>')
    t = ("AREX Mining — Exploración y desarrollo de proyectos mineros en Argentina" if lang == "es"
         else "AREX Mining — Mineral exploration and mining project development in Argentina")
    d = ("AREX Mining desarrolla el proyecto de cobre San Romeleo, en Mendoza, y el Proyecto Tres Cruces de litio, en Catamarca, Argentina." if lang == "es"
         else "AREX Mining develops the San Romeleo copper project in Mendoza and the Tres Cruces lithium project in Catamarca, Argentina.")
    return t, d, body
PAGES["index"] = home

def about(lang):
    if lang == "es":
        h = page_hero("Nosotros", "Experiencia probada en el desarrollo de proyectos",
                      "AREX Mining S.A. es una empresa argentina de servicios mineros. Nuestro equipo desarrolla proyectos de cobre y litio para sus titulares, desde la exploración hasta la producción.")
        who = ('<span class="eyebrow">Quiénes somos</span><h2>Desarrolladores de proyectos mineros</h2>'
               '<p>AREX Mining reúne a profesionales con amplia trayectoria en la exploración, el estudio, la aprobación y la construcción de proyectos mineros en Argentina y en el exterior.</p>'
               '<p>Trabajamos junto a los titulares de los proyectos para llevar su proyecto al mercado.</p>')
        track = ('<span class="eyebrow">Trayectoria</span><h2>Lo hicimos antes</h2>'
                 '<p>Nuestro equipo cuenta con experiencia en algunos de los mayores proyectos mineros y de exploración de África, Europa y Oceanía.</p>'
                 '<p>En Argentina, integrantes de nuestro equipo participaron en el desarrollo del proyecto Cauchari, de Lithium Americas, y del proyecto Tres Quebradas (3Q), de Neo Lithium. Hoy aplicamos esa experiencia a una nueva cartera de proyectos de cobre y litio.</p>')
        how_h = ("Cómo trabajamos", "Una sola organización para todo el ciclo del proyecto")
        how = ["Exploración y geología", "Estudios e ingeniería", "Comunidad y ambiente",
               "Permisos y aprobaciones", "Construcción y puesta en marcha"]
        vals = ("Lo que nos guía", "Misión, visión y valores")
    else:
        h = page_hero("About", "Proven experience in project development",
                      "AREX Mining S.A. is an Argentine mining services company. Our team develops copper and lithium projects for their owners, from exploration through to production.")
        who = ('<span class="eyebrow">Who we are</span><h2>Mining project developers</h2>'
               '<p>AREX Mining brings together professionals with long track records in exploring, studying, permitting and building mining projects in Argentina and internationally.</p>'
               '<p>We work with project owners to bring their project to market.</p>')
        track = ('<span class="eyebrow">Track record</span><h2>We have done this before</h2>'
                 '<p>Our team has experience working across some of the largest mining and exploration projects in Africa, Europe and Oceania.</p>'
                 '<p>In Argentina, members of our team helped develop Lithium Americas\' Cauchari project and Neo Lithium\'s Tres Quebradas (3Q) project. We are now bringing that experience to a new portfolio of copper and lithium projects.</p>')
        how_h = ("How we work", "One organisation for the whole project lifecycle")
        how = ["Exploration and geology", "Studies and engineering", "Community and environment",
               "Permitting and approvals", "Construction and commissioning"]
        vals = ("What guides us", "Mission, vision and values")
    checks = '<ol class="flow">' + "".join(f'<li><span class="flow-n">{i:02d}</span><span class="flow-t">{x}</span></li>' for i, x in enumerate(how, 1)) + '</ol>'
    alt = ("Integrantes del equipo revisan un mapa geológico y una maqueta del terreno durante una reunión de trabajo" if lang == "es"
           else "Team members reviewing a geological map and a terrain model during a working meeting")
    body = (h + f'<section><div class="wrap split" style="align-items:start"><div>{who}</div><div>{track}</div></div>'
            f'<div class="wrap"><img class="wide-photo" src="team-map.jpg" alt="{alt}" width="1800" height="736" loading="lazy"></div></section>'
            f'<section class="has-contour">{CONTOUR}<div class="wrap narrow"><span class="eyebrow">{how_h[0]}</span><h2>{how_h[1]}</h2>{checks}</div></section>'
            f'<section class="section-deep"><div class="wrap"><span class="eyebrow">{vals[0]}</span><h2>{vals[1]}</h2>{values_block(lang)}</div></section>')
    t = "Nosotros — AREX Mining" if lang == "es" else "About — AREX Mining"
    d = ("AREX Mining S.A. es una empresa argentina de servicios mineros que desarrolla proyectos de cobre y litio." if lang == "es"
         else "AREX Mining S.A. is an Argentine mining services company developing copper and lithium projects.")
    return t, d, body
PAGES["about"] = about

def services(lang):
    if lang == "es":
        h = page_hero("Servicios", "De la exploración a la producción",
                      "Acompañamos a los titulares de proyectos mineros en cada etapa, con un equipo que cubre todas las disciplinas que requiere un proyecto exitoso.")
        intro = ("Lo que hacemos", "Servicios de desarrollo de proyectos")
        disc_h = ("Disciplinas", "Todas las disciplinas, en un solo equipo")
        disc = ("Nuestro equipo cubre cada disciplina que requiere el desarrollo de un proyecto: legales, ambiente, relaciones comunitarias, logística, geología e hidrogeología, procesamiento, pruebas piloto y ensayos, construcción, puesta en marcha y producción.")
        cta = ("¿Tiene un proyecto?", "Conversemos sobre cómo podemos ayudarle a desarrollarlo.", "Contactar")
    else:
        h = page_hero("Services", "From exploration to production",
                      "We support mining project owners at every stage, with a team that covers every discipline a successful project requires.")
        intro = ("What we do", "Project development services")
        disc_h = ("Disciplines", "Every discipline, in one team")
        disc = ("Our team covers every discipline that project development requires: legal, environment, community relations, logistics, geology and hydrogeology, processing, piloting and testing, construction, commissioning and production.")
        cta = ("Have a project?", "Let's talk about how we can help you develop it.", "Get in touch")
    body = (h + f'<section><div class="wrap"><span class="eyebrow">{intro[0]}</span><h2>{intro[1]}</h2>{services_grid(lang)}</div></section>'
            f'<section class="section-deep"><div class="wrap narrow"><span class="eyebrow">{disc_h[0]}</span><h2>{disc_h[1]}</h2><p class="lede">{disc}</p></div></section>'
            f'<section class="section-tint"><div class="wrap narrow"><h2>{cta[0]}</h2><p class="lede">{cta[1]}</p>'
            f'<p style="margin-top:1.8rem"><a class="btn" href="{href("contact", lang)}">{cta[2]}</a></p></div></section>')
    t = "Servicios — AREX Mining" if lang == "es" else "Services — AREX Mining"
    d = ("Exploración, estudios, permisos, comunidad y ambiente, construcción y puesta en marcha de proyectos mineros." if lang == "es"
         else "Exploration, studies, permitting, community and environment, construction and commissioning of mining projects.")
    return t, d, body
PAGES["services"] = services

def mineral_page(slug, eyebrow, title, spiel, proj_slug, kicker, ptitle, ptext, lang, meta_title, meta_desc, img=None, alt=""):
    body = (page_hero(eyebrow, title, spiel, tall=True, img=img, alt=alt) +
            f'<section><div class="wrap"><span class="eyebrow">{"Proyectos" if lang == "es" else "Projects"}</span>'
            f'<h2>{"Nuestro proyecto" if lang == "es" else "Our project"}</h2>'
            f'<div class="grid grid-2" style="margin-top:2rem">{project_card(lang, proj_slug, kicker, ptitle, ptext)}</div></div></section>')
    return meta_title, meta_desc, body

def copper(lang):
    if lang == "es":
        return mineral_page("copper", "Proyectos · Cobre", "Cobre",
            "Desde hace miles de años, el cobre acompaña la ambición humana: de las primeras herramientas a los cables que iluminan nuestras ciudades. Hoy es la corriente silenciosa de la transición energética, presente en cada red eléctrica, vehículo eléctrico, aerogenerador y parque solar. También trabaja la tierra: como sulfato de cobre protege viñedos, frutales y cultivos de las enfermedades, y como micronutriente nutre los suelos y el ganado. A medida que el mundo se electrifica y crece, esa corriente se fortalece, y en los altos valles de la cordillera argentina se encuentran algunos de los yacimientos sin desarrollar más prometedores de la región, listos para impulsar lo que viene.",
            "san-romeleo", "Cobre · Malargüe, Mendoza", "San Romeleo",
            "Reactivación productiva de un cuerpo de cobre oxidado y exploración del distrito, desarrollado para AREX Copper.",
            lang, "Cobre — AREX Mining", "Por qué el cobre es esencial para la transición energética, y el proyecto San Romeleo en Mendoza.",
            img="copper-banner.jpg", alt="Paisaje cordillerano en Malargüe, Mendoza")
    return mineral_page("copper", "Projects · Copper", "Copper",
        "For thousands of years, copper has carried human ambition, from the first tools to the wires that light our cities. Today it is the quiet current of the energy transition, running through every power grid, electric vehicle, wind turbine and solar farm. It works the land too: as copper sulphate it protects vineyards, orchards and crops from disease, and as a micronutrient it nourishes soils and livestock. As the world electrifies and grows, that current grows stronger, and in the high valleys of Argentina's Andes lie some of the region's most promising undeveloped deposits, waiting to power what comes next.",
        "san-romeleo", "Copper · Malargüe, Mendoza", "San Romeleo",
        "Productive reactivation of an oxidised copper body and exploration of the surrounding district, developed for AREX Copper.",
        lang, "Copper — AREX Mining", "Why copper is essential to the energy transition, and the San Romeleo project in Mendoza.",
        img="copper-banner.jpg", alt="Andean landscape in Malargüe, Mendoza")
PAGES["copper"] = copper

def lithium(lang):
    if lang == "es":
        return mineral_page("lithium", "Proyectos · Litio", "Litio",
            "El litio es el componente clave de las baterías recargables que impulsan los vehículos eléctricos y almacenan energía renovable. Argentina forma parte del Triángulo del Litio, junto con Chile y Bolivia, que concentra una gran parte de los recursos de litio del mundo.",
            "tres-cruces", "Litio · Catamarca", "Proyecto Tres Cruces",
            "Depósito de salmuera de litio de grado batería en la Puna catamarqueña, desarrollado para 3C Resources.",
            lang, "Litio — AREX Mining", "Por qué el litio es clave para las baterías y la energía renovable, y el Proyecto Tres Cruces en Catamarca.")
    return mineral_page("lithium", "Projects · Lithium", "Lithium",
        "Lithium is the key ingredient in the rechargeable batteries that power electric vehicles and store renewable energy. Argentina is part of the Lithium Triangle with Chile and Bolivia, which holds a large share of the world's lithium resources.",
        "tres-cruces", "Lithium · Catamarca", "The Tres Cruces Project",
        "A battery-grade lithium brine deposit on the Catamarca Puna, developed for 3C Resources.",
        lang, "Lithium — AREX Mining", "Why lithium is key to batteries and renewable energy, and the Tres Cruces Project in Catamarca.")
PAGES["lithium"] = lithium

def coming(lang, mineral_es, mineral_en, slug):
    if lang == "es":
        body = (page_hero(f"Proyectos · {mineral_es}", mineral_es) +
                '<section><div class="wrap"><p class="notice">Tenemos varios proyectos en desarrollo. Vuelva a visitarnos más adelante para obtener más información.</p></div></section>')
        return f"{mineral_es} — AREX Mining", f"Proyectos de {mineral_es.lower()} en desarrollo de AREX Mining.", body
    body = (page_hero(f"Projects · {mineral_en}", mineral_en) +
            '<section><div class="wrap"><p class="notice">We have several projects in development. Check back later for more information.</p></div></section>')
    return f"{mineral_en} — AREX Mining", f"AREX Mining's {mineral_en.lower()} projects in development.", body
PAGES["gold"] = lambda lang: coming(lang, "Oro", "Gold", "gold")
PAGES["silver"] = lambda lang: coming(lang, "Plata", "Silver", "silver")

def san_romeleo(lang):
    if lang == "es":
        h = page_hero("Cobre · Malargüe, Mendoza", "San Romeleo", "Proyecto de cobre desarrollado por AREX Mining para AREX Copper.")
        strip = [("Cobre", "óxidos de cobre"), ("Malargüe", "provincia de Mendoza"), ("AREX Copper", "desarrollado para"), ("AREX Mining S.A.", "operador")]
        intro = ('<span class="eyebrow">El proyecto</span><h2>Una propiedad, dos etapas en paralelo</h2>'
                 '<p>San Romeleo es una propiedad minera ubicada en el departamento de Malargüe, en el sur de la provincia de Mendoza. El proyecto, impulsado originalmente por LABSA S.A., es operado hoy por AREX Mining S.A. y se desarrolla para AREX Copper.</p>'
                 '<p>El proyecto avanza por dos vías administrativas sobre el mismo activo minero, cada una con su propia evaluación ambiental, alcances claramente definidos y sin superposición de permisos.</p>')
        tracks_h = ("Etapas", "Cómo avanza San Romeleo")
        tracks = [("Reactivación productiva", "Un expediente individual para la explotación, a pequeña escala, de un cuerpo de cobre oxidado y la operación de una planta de procesamiento para la producción de sulfato de cobre."),
                  ("Exploración", "La propiedad forma parte del tercer grupo del Distrito Minero Malargüe Occidental (MDMO III), actualmente en evaluación ambiental. Las tareas previstas incluyen mapeo geológico de superficie, muestreo, estudios geofísicos y perforación diamantina, junto con obras auxiliares de bajo impacto.")]
        role_h = ("Nuestro rol", "Lo que aporta AREX Mining")
        role = ["Gestión de permisos y evaluaciones ambientales", "Planificación y ejecución de la exploración",
                "Ingeniería y desarrollo de la planta de procesamiento", "Relación con autoridades y comunidades de Malargüe"]
    else:
        h = page_hero("Copper · Malargüe, Mendoza", "San Romeleo", "A copper project developed by AREX Mining for AREX Copper.")
        strip = [("Copper", "copper oxides"), ("Malargüe", "Mendoza province"), ("AREX Copper", "developed for"), ("AREX Mining S.A.", "operator")]
        intro = ('<span class="eyebrow">The project</span><h2>One property, two tracks in parallel</h2>'
                 '<p>San Romeleo is a mining property in the department of Malargüe, in the south of Mendoza province. Originally promoted by LABSA S.A., the project is now operated by AREX Mining S.A. and developed for AREX Copper.</p>'
                 '<p>The project is advancing along two administrative tracks over the same mining asset, each with its own environmental assessment, clearly defined scope and no overlapping permits.</p>')
        tracks_h = ("Tracks", "How San Romeleo is advancing")
        tracks = [("Productive reactivation", "An individual file for the small-scale mining of an oxidised copper body and the operation of a processing plant to produce copper sulphate."),
                  ("Exploration", "The property is part of the third group of the Malargüe Western Mining District (MDMO III), currently under environmental assessment. Planned work includes surface geological mapping, sampling, geophysical studies and diamond drilling, along with low-impact auxiliary works.")]
        role_h = ("Our role", "What AREX Mining brings")
        role = ["Permitting and environmental assessments", "Exploration planning and execution",
                "Engineering and development of the processing plant", "Engagement with Malargüe authorities and communities"]
    strip_html = '<div class="strip"><div class="wrap">' + "".join(f'<div class="cell"><b>{b}</b><span>{s}</span></div>' for b, s in strip) + '</div></div>'
    tcards = '<div class="grid grid-2" style="margin-top:2.2rem">' + "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in tracks) + '</div>'
    checks = '<div class="roles">' + "".join(f'<div class="role"><span class="role-n">{i:02d}</span><p>{x}</p></div>' for i, x in enumerate(role, 1)) + '</div>'
    body = (h + strip_html +
            f'<section class="section-deep"><div class="wrap map-panel">{arg_map(["sr"], "San Romeleo · Malargüe, Mendoza")}<div>{intro}</div></div></section>'
            f'<section><div class="wrap"><span class="eyebrow">{tracks_h[0]}</span><h2>{tracks_h[1]}</h2>{tcards}</div></section>'
            f'<section class="section-alt"><div class="wrap"><span class="eyebrow">{role_h[0]}</span><h2>{role_h[1]}</h2>{checks}</div></section>')
    t = "San Romeleo — Proyecto de cobre en Malargüe, Mendoza — AREX Mining" if lang == "es" else "San Romeleo — Copper project in Malargüe, Mendoza — AREX Mining"
    d = ("San Romeleo es un proyecto de cobre en Malargüe, Mendoza, desarrollado por AREX Mining para AREX Copper." if lang == "es"
         else "San Romeleo is a copper project in Malargüe, Mendoza, developed by AREX Mining for AREX Copper.")
    return t, d, body
PAGES["san-romeleo"] = san_romeleo

def tres_cruces(lang):
    if lang == "es":
        h = page_hero("Litio · Catamarca", "Proyecto Tres Cruces", "Proyecto de litio desarrollado por el equipo de AREX Mining para 3C Resources.")
        strip = [("Litio", "salmuera de grado batería"), ("Catamarca", "Puna, Argentina"), ("3C Resources", "desarrollado para"), ("Minera Cordillera", "operadora")]
        intro = ('<span class="eyebrow">El proyecto</span><h2>Litio de grado batería en la Puna</h2>'
                 '<p>El Proyecto Tres Cruces es un depósito de litio de gran escala y grado batería en la provincia de Catamarca, en el noroeste argentino, a unos 30 km de la frontera con Chile y a 154 km de Fiambalá.</p>'
                 '<p>Se ubica en torno al volcán Tres Cruces y al cono aluvial junto al salar de Tres Quebradas. El proyecto pertenece a 3C Resources y es operado por su subsidiaria Minera Cordillera, que posee o tiene derechos sobre aproximadamente 30.000 hectáreas en la cuenca.</p>')
        stage_h = ("Estado", "Hacia la producción")
        stages = [("2025", "La geofísica confirma el acuífero hipersalino y se completan los primeros cuatro pozos de perforación."),
                  ("2026", "Diez pozos completados. Estudio de prefactibilidad finalizado y estudio de factibilidad en curso."),
                  ("2028 – 2029", "Inicio de producción previsto, con una meta inicial de 20.000 toneladas anuales y la posibilidad de llegar a 40.000.")]
        role_h = ("Nuestro rol", "Lo que aporta AREX Mining")
        role = ["Gestión de estudios, ingeniería y desarrollo de procesos", "Exploración, perforación e hidrogeología",
                "Permisos, evaluaciones ambientales y relaciones comunitarias", "Gobierno corporativo y relación con inversores"]
        ext = ("Más información sobre el proyecto en el sitio de 3C Resources", "Visitar 3cresources.com")
    else:
        h = page_hero("Lithium · Catamarca", "The Tres Cruces Project", "A lithium project developed by the AREX Mining team for 3C Resources.")
        strip = [("Lithium", "battery-grade brine"), ("Catamarca", "Puna, Argentina"), ("3C Resources", "developed for"), ("Minera Cordillera", "operator")]
        intro = ('<span class="eyebrow">The project</span><h2>Battery-grade lithium on the Puna</h2>'
                 '<p>The Tres Cruces Project is a large-scale, battery-grade lithium deposit in the Catamarca Province of north-west Argentina, approximately 30 km from the Chilean border and 154 km from Fiambalá.</p>'
                 '<p>It is centred on the Tres Cruces volcano and the alluvial cone beside the Tres Quebradas salar. The project is owned by 3C Resources and operated by its subsidiary Minera Cordillera, which owns or holds rights over approximately 30,000 hectares in the basin.</p>')
        stage_h = ("Status", "Towards production")
        stages = [("2025", "Geophysics confirms the hyper-saline aquifer and the first four drill holes are completed."),
                  ("2026", "Ten drill holes completed. Pre-feasibility study finished and feasibility study under way."),
                  ("2028 – 2029", "Targeted start of production, initially 20,000 tonnes per annum with a pathway to 40,000.")]
        role_h = ("Our role", "What AREX Mining brings")
        role = ["Management of studies, engineering and process development", "Exploration, drilling and hydrogeology",
                "Permitting, environmental assessments and community relations", "Corporate governance and investor relations"]
        ext = ("More about the project on the 3C Resources website", "Visit 3cresources.com")
    strip_html = '<div class="strip"><div class="wrap">' + "".join(f'<div class="cell"><b>{b}</b><span>{s}</span></div>' for b, s in strip) + '</div></div>'
    tl = '<ol class="timeline">' + "".join(f'<li><b>{a}</b><p>{b}</p></li>' for a, b in stages) + '</ol>'
    checks = '<div class="roles">' + "".join(f'<div class="role"><span class="role-n">{i:02d}</span><p>{x}</p></div>' for i, x in enumerate(role, 1)) + '</div>'
    body = (h + strip_html +
            f'<section class="section-deep"><div class="wrap map-panel">{arg_map(["tc"], "Tres Cruces · Catamarca")}<div>{intro}</div></div></section>'
            f'<section class="section-teal"><div class="wrap narrow"><span class="eyebrow">{stage_h[0]}</span><h2>{stage_h[1]}</h2>{tl}</div></section>'
            f'<section class="section-alt"><div class="wrap"><span class="eyebrow">{role_h[0]}</span><h2>{role_h[1]}</h2>{checks}'
            f'<p style="margin-top:2.2rem">{ext[0]}.</p><p style="margin-top:1rem"><a class="btn" href="https://www.3cresources.com" target="_blank" rel="noopener">{ext[1]}</a></p></div></section>')
    t = "Proyecto Tres Cruces — Litio en Catamarca — AREX Mining" if lang == "es" else "The Tres Cruces Project — Lithium in Catamarca — AREX Mining"
    d = ("El Proyecto Tres Cruces es un depósito de litio de grado batería en Catamarca, desarrollado por el equipo de AREX Mining para 3C Resources." if lang == "es"
         else "The Tres Cruces Project is a battery-grade lithium deposit in Catamarca, developed by the AREX Mining team for 3C Resources.")
    return t, d, body
PAGES["tres-cruces"] = tres_cruces

def people(lang):
    if lang == "es":
        return "Nuestra gente — AREX Mining", "El equipo de AREX Mining.", page_hero("Nuestra gente", "Nuestra gente", tall=True)
    return "Our People — AREX Mining", "The AREX Mining team.", page_hero("Our People", "Our People", tall=True)
PAGES["people"] = people

def lab(lang):
    if lang == "es":
        body = (page_hero("Nuestro laboratorio", "Nuestro laboratorio") +
                '<section class="section-alt" style="border-bottom:none"><div class="wrap narrow"><p class="lede">Nuestras instalaciones se encuentran entre las más avanzadas de Argentina e incluyen un laboratorio y capacidades de I+D dedicados a la investigación de tecnologías de litio, con capacidad para hasta 100 ingenieros y profesionales de proyecto.</p></div></section>'
                '<section class="section-alt" style="padding-top:0;border-top:none"><div class="wrap"><div class="photo-grid">'
                '<img src="lab-team.jpg" alt="Dos científicas revisan resultados en el laboratorio" width="926" height="520" loading="lazy">'
                '<img src="lab-icp.jpg" alt="Un técnico prepara muestras para análisis por espectrometría en el laboratorio" width="928" height="618" loading="lazy">'
                '</div></div></section>')
        return ("Nuestro laboratorio — AREX Mining",
                "Laboratorio e instalaciones de I+D de AREX Mining, dedicados a la investigación de tecnologías de litio.", body)
    body = (page_hero("Our Lab", "Our Lab") +
            '<section class="section-alt" style="border-bottom:none"><div class="wrap narrow"><p class="lede">Our facilities are among the most advanced in Argentina and include a laboratory and R&amp;D capabilities dedicated to researching lithium technologies and capacity for up to 100 engineers and project professionals.</p></div></section>'
            '<section class="section-alt" style="padding-top:0;border-top:none"><div class="wrap"><div class="photo-grid">'
            '<img src="lab-team.jpg" alt="Two scientists reviewing results together in the laboratory" width="926" height="520" loading="lazy">'
            '<img src="lab-icp.jpg" alt="A technician preparing samples for spectrometry analysis in the laboratory" width="928" height="618" loading="lazy">'
            '</div></div></section>')
    return ("Our Lab — AREX Mining",
            "AREX Mining's laboratory and R&amp;D facilities, dedicated to researching lithium technologies.", body)
PAGES["lab"] = lab


def esg(lang):
    if lang == "es":
        h = page_hero("Sustentabilidad", "Desarrollo minero responsable",
                      "Generamos proyectos mineros en armonía con el ambiente, respetando a las comunidades locales y contribuyendo efectivamente al desarrollo del país.")
        com_h = ("Nuestros compromisos", "Cómo desarrollamos cada proyecto")
        coms = [("Ambiente", "Integramos la evaluación y el monitoreo ambiental desde las primeras etapas de cada proyecto, con sistemas de gestión de riesgos, cumplimiento normativo y mejora continua."),
                ("Agua", "Tratamos la gestión del agua como un eje central del diseño de cada proyecto, cuidando el acceso de las comunidades a sus fuentes de agua."),
                ("Comunidades", "Mantenemos una comunicación clara y continua con las comunidades cercanas a nuestros proyectos, desde la exploración hasta la operación."),
                ("Empleo y proveedores locales", "Priorizamos la contratación de personas y proveedores de las provincias donde trabajamos."),
                ("Transparencia", "Actuamos con transparencia, honestidad y confianza en nuestra relación con autoridades, comunidades, socios e inversores."),
                ("Gobierno corporativo", "Aplicamos prácticas de gobierno corporativo sólidas y rendimos cuentas a los titulares de los proyectos que desarrollamos.")]
        auth_h = ("Trabajo conjunto", "Con autoridades y comunidades")
        auth = "Trabajamos junto a las autoridades provinciales, especialistas técnicos y las comunidades locales para asegurar decisiones transparentes, una gestión ambiental eficaz y la protección del entorno durante todo el ciclo de vida de cada proyecto."
    else:
        h = page_hero("ESG", "Responsible mining development",
                      "We develop mining projects in harmony with the environment, respecting local communities and contributing meaningfully to the country's development.")
        com_h = ("Our commitments", "How we develop every project")
        coms = [("Environment", "We build environmental assessment and monitoring into each project from its earliest stages, with systems for risk management, compliance and continuous improvement."),
                ("Water", "We treat water management as central to each project's design, safeguarding communities' access to their water sources."),
                ("Communities", "We maintain clear and continuous communication with the communities near our projects, from exploration through to operation."),
                ("Local jobs and suppliers", "We prioritise hiring people and suppliers from the provinces where we work."),
                ("Transparency", "We act with transparency, honesty and trust in our dealings with authorities, communities, partners and investors."),
                ("Governance", "We apply sound corporate governance practices and are accountable to the owners of the projects we develop.")]
        auth_h = ("Working together", "With authorities and communities")
        auth = "We work alongside provincial authorities, technical specialists and local communities to ensure transparent decision-making, effective environmental management and protection of the surrounding environment throughout each project's life."
    cards = '<div class="grid grid-3" style="margin-top:2.2rem">' + "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in coms) + '</div>'
    body = (h + f'<section class="has-contour">{CONTOUR}<div class="wrap"><span class="eyebrow">{com_h[0]}</span><h2>{com_h[1]}</h2>{cards}</div></section>'
            f'<section class="section-teal"><div class="wrap narrow"><span class="eyebrow">{auth_h[0]}</span><h2>{auth_h[1]}</h2><p class="lede">{auth}</p></div></section>')
    t = "Sustentabilidad — AREX Mining" if lang == "es" else "ESG — AREX Mining"
    d = ("Compromisos ambientales, sociales y de gobierno corporativo de AREX Mining." if lang == "es"
         else "AREX Mining's environmental, social and governance commitments.")
    return t, d, body
PAGES["esg"] = esg

def news(lang):
    PR1 = "https://prensa.mendoza.gob.ar/amplio-apoyo-en-la-audiencia-publica-del-proyecto-cobre-san-romeleo-en-malargue/"
    PR2 = "https://www.memo.com.ar/economia/proyecto-minero-san-romeleo/"
    PR3 = "https://prensa.mendoza.gob.ar/energia-y-ambiente-convoca-a-la-audiencia-publica-del-proyecto-cobre-san-romeleo/"
    PR4 = "https://www.diariouno.com.ar/politica/mendoza-suma-otro-proyecto-cuprifero-y-va-audiencia-publica-cobre-san-romeleo-malargue-n1494636"
    if lang == "es":
        h = page_hero("Novedades", "Novedades de nuestros proyectos")
        more = "Leer más"
        items = [("2026", "San Romeleo", "San Romeleo se incorpora al Distrito Minero Malargüe Occidental",
                  "La propiedad San Romeleo fue incluida en el tercer grupo del Distrito Minero Malargüe Occidental (MDMO III), actualmente en evaluación ambiental, que prevé tareas de mapeo, muestreo, geofísica y perforación diamantina. En paralelo, avanza el expediente para la reactivación productiva del proyecto.",
                  "news-copper-outcrop.jpg", "Mineralización de cobre en un afloramiento de San Romeleo, junto a un martillo de geólogo", None),
                 ("Junio 2026", "Tres Cruces", "Presentación del Informe de Impacto Ambiental de exploración",
                  "Se presentó un Informe de Impacto Ambiental para la etapa de exploración del Proyecto Tres Cruces, con el objetivo de extender el permiso de exploración vigente por dos años. Más de 250 personas participaron en la consulta comunitaria sobre el proyecto, realizada en Fiambalá.",
                  "news-consultation.jpg", "Más de 250 personas asisten a la consulta comunitaria del Proyecto Tres Cruces en Fiambalá", None),
                 ("Abril 2026", "Tres Cruces", "Ausenco, designada para el estudio de prefactibilidad",
                  "La firma global de ingeniería Ausenco fue designada para completar el estudio de prefactibilidad del Proyecto Tres Cruces.", None, None, None),
                 ("Diciembre 2025", "San Romeleo", "Amplio apoyo en la audiencia pública del Proyecto Cobre San Romeleo en Malargüe",
                  "El Proyecto Cobre San Romeleo obtuvo un amplio respaldo durante la audiencia pública realizada en Malargüe, con más del 90 % de adhesiones por parte de ciudadanos y representantes de diversos sectores productivos, sociales y académicos. La audiencia, presencial y virtual, se realizó en el marco de la evaluación del Informe de Impacto Ambiental y fue organizada por la Dirección de Minería y la Dirección de Gestión y Fiscalización Ambiental del Ministerio de Energía y Ambiente.",
                  "news-hearing.jpg", "Participantes de la audiencia pública del proyecto San Romeleo en Malargüe", PR1),
                 ("Diciembre 2025", "San Romeleo", "Taller participativo del proyecto San Romeleo previo a la audiencia pública",
                  "La Autoridad Ambiental Minera convocó a la comunidad a un taller participativo sobre el proyecto San Romeleo, realizado el 2 de diciembre de 2025 en Malargüe en modalidad presencial y virtual, para brindar información sobre el proyecto y sus informes técnicos.",
                  "news-valley.jpg", "Paisaje del área del proyecto San Romeleo, en Malargüe, Mendoza", PR2),
                 ("Noviembre 2025", "San Romeleo", "Energía y Ambiente convoca a audiencia pública para el proyecto Cobre San Romeleo",
                  "La Autoridad Ambiental Minera convocó a la audiencia pública del proyecto Cobre San Romeleo, orientado a la producción de óxido de cobre, para el 6 de diciembre de 2025, en modalidad híbrida, con participación presencial en la zona del proyecto en Malargüe y opción virtual.",
                  "news-field.jpg", "Recorrida de campo en el área del proyecto San Romeleo", PR3),
                 ("Noviembre 2025", "San Romeleo", "Mendoza suma otro proyecto cuprífero y va a audiencia pública",
                  "Las autoridades provinciales convocaron a la audiencia pública del proyecto Cobre San Romeleo, en la que se presentó su Informe de Impacto Ambiental. El expediente cuenta con dictámenes favorables de organismos especializados, instituciones académicas y autoridades locales.",
                  "news-briefing.jpg", "Presentación técnica del proyecto San Romeleo", PR4)]
    else:
        h = page_hero("News", "News from our projects")
        more = "Read more (in Spanish)"
        items = [("2026", "San Romeleo", "San Romeleo joins the Malargüe Western Mining District",
                  "The San Romeleo property has been included in the third group of the Malargüe Western Mining District (MDMO III), currently under environmental assessment, which provides for mapping, sampling, geophysics and diamond drilling. In parallel, the file for the project's productive reactivation is advancing.",
                  "news-copper-outcrop.jpg", "Copper mineralisation in an outcrop at San Romeleo, beside a geologist's hammer", None),
                 ("June 2026", "Tres Cruces", "Exploration Environmental Impact Assessment submitted",
                  "An Environmental Impact Assessment was submitted for the exploration stage of the Tres Cruces Project, to extend the existing exploration permit by two years. The community consultation on the project, held in Fiambalá, was attended by more than 250 people.",
                  "news-consultation.jpg", "More than 250 people attending the Tres Cruces Project community consultation in Fiambalá", None),
                 ("April 2026", "Tres Cruces", "Ausenco appointed to complete pre-feasibility study",
                  "Global engineering firm Ausenco was appointed to complete the Pre-Feasibility Study for the Tres Cruces Project.", None, None, None),
                 ("December 2025", "San Romeleo", "Broad support at the San Romeleo Copper Project public hearing in Malargüe",
                  "The San Romeleo Copper Project received broad support at the public hearing held in Malargüe, with more than 90% of participants, including citizens and representatives of productive, social and academic sectors, speaking in favour. The hearing, held in person and online, formed part of the Environmental Impact Assessment review and was organised by the Mining Directorate and the Environmental Management and Oversight Directorate of the Ministry of Energy and Environment.",
                  "news-hearing.jpg", "Participants at the San Romeleo project public hearing in Malargüe", PR1),
                 ("December 2025", "San Romeleo", "Community workshop on San Romeleo ahead of the public hearing",
                  "The Mining Environmental Authority invited the community to a participatory workshop on the San Romeleo project, held on 2 December 2025 in Malargüe in person and online, to share information about the project and its technical reports.",
                  "news-valley.jpg", "Landscape of the San Romeleo project area in Malargüe, Mendoza", PR2),
                 ("November 2025", "San Romeleo", "Public hearing called for the San Romeleo Copper Project",
                  "The Mining Environmental Authority called a public hearing for the San Romeleo Copper Project, which will produce copper oxide, for 6 December 2025, in a hybrid format with in-person participation near the project in Malargüe and an online option.",
                  "news-field.jpg", "Field visit to the San Romeleo project area", PR3),
                 ("November 2025", "San Romeleo", "Mendoza adds another copper project and goes to public hearing",
                  "Provincial authorities called the public hearing for the San Romeleo Copper Project, at which its Environmental Impact Assessment was presented. The file has favourable opinions from specialist agencies, academic institutions and local authorities.",
                  "news-briefing.jpg", "Technical presentation of the San Romeleo project", PR4)]
    rows = []
    for d, tag, t, p, img, alt, link in items:
        pic = f'<img class="news-img" src="{img}" alt="{alt}" loading="lazy">' if img else ""
        lk = f'<p class="news-link"><a href="{link}" target="_blank" rel="noopener">{more} →</a></p>' if link else ""
        cls = "news-item has-img" if img else "news-item"
        rows.append(f'<article class="{cls}"><time>{d}</time><div><span class="news-tag">{tag}</span><h2>{t}</h2><p>{p}</p>{lk}</div>{pic}</article>')
    body = h + f'<section><div class="wrap">{"".join(rows)}</div></section>'
    t = "Novedades — AREX Mining" if lang == "es" else "News — AREX Mining"
    d = ("Novedades de los proyectos San Romeleo y Tres Cruces." if lang == "es" else "News from the San Romeleo and Tres Cruces projects.")
    return t, d, body
PAGES["news"] = news

FORM_TO = "REEMPLAZAR-CON-EMAIL@arexmining.com"

def contact(lang):
    if lang == "es":
        h = page_hero("Contacto", "Envíe su consulta",
                      "Titulares de proyectos, inversores, proveedores, miembros de la comunidad y medios: envíe su mensaje y la persona indicada le responderá.")
        f = dict(eb="Formulario", h2="Escríbanos", subj="Consulta desde el sitio web de AREX Mining", name="Nombre", pos="Cargo",
                 co="Empresa", email="Correo electrónico", msg="Mensaje", send="Enviar consulta",
                 note='Los campos marcados con <span class="req">*</span> son obligatorios.',
                 priv=f'Los datos personales que nos proporcione se utilizarán únicamente para responder a su consulta y llevar un registro de la correspondencia. Consulte nuestra <a href="{href("privacy", lang)}">Política de Privacidad</a> para conocer sus derechos de acceso, rectificación y supresión.',
                 draft="Falta la dirección de correo electrónico que recibirá las consultas del formulario.",
                 where_eb="Dónde trabajamos", where_h="Mendoza y Catamarca, Argentina",
                 where=["Desarrollamos el proyecto de cobre San Romeleo en el departamento de Malargüe, Mendoza, y el Proyecto Tres Cruces en la provincia de Catamarca."])
    else:
        h = page_hero("Contact", "Submit an enquiry",
                      "Project owners, investors, suppliers, community members and media: send a message and the right person will come back to you.")
        f = dict(eb="Enquiry form", h2="Get in touch", subj="Enquiry via the AREX Mining website", name="Name", pos="Position",
                 co="Company", email="Email", msg="Message", send="Send enquiry",
                 note='Fields marked <span class="req">*</span> are required.',
                 priv=f'The personal data you provide will be used only to respond to your enquiry and to keep a record of correspondence. See our <a href="{href("privacy", lang)}">Privacy Policy</a> for your rights of access, correction and deletion.',
                 draft="The email address that will receive enquiries from this form is still needed.",
                 where_eb="Where we work", where_h="Mendoza and Catamarca, Argentina",
                 where=["We are developing the San Romeleo copper project in the department of Malargüe, Mendoza, and the Tres Cruces Project in Catamarca Province."])
    req = '<span class="req">*</span>'
    form = (f'<form id="enquiry" action="https://formsubmit.co/{FORM_TO}" method="POST">'
            f'<input type="hidden" name="_subject" value="{f["subj"]}">'
            '<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
            f'<label for="name">{f["name"]} {req}</label><input id="name" type="text" name="name" required autocomplete="name">'
            f'<label for="position">{f["pos"]} {req}</label><input id="position" type="text" name="position" required autocomplete="organization-title">'
            f'<label for="company">{f["co"]} {req}</label><input id="company" type="text" name="company" required autocomplete="organization">'
            f'<label for="email">{f["email"]} {req}</label><input id="email" type="email" name="email" required autocomplete="email">'
            f'<label for="message">{f["msg"]}</label><textarea id="message" name="message"></textarea>'
            f'<button class="btn" type="submit">{f["send"]}</button><p class="formnote">{f["note"]}</p>'
            f'<p class="privacy-notice">{f["priv"]}</p></form>')
    where = "".join(f"<p>{p}</p>" for p in f["where"])
    body = (h + f'<section><div class="wrap split" style="align-items:start"><div><span class="eyebrow">{f["eb"]}</span><h2>{f["h2"]}</h2>'
            f'<div class="draft">{f["draft"]}</div>{form}</div>'
            f'<div><span class="eyebrow">{f["where_eb"]}</span><h2>{f["where_h"]}</h2>{where}</div></div></section>')
    t = "Contacto — AREX Mining" if lang == "es" else "Contact — AREX Mining"
    d = ("Contacte a AREX Mining." if lang == "es" else "Contact AREX Mining.")
    return t, d, body
PAGES["contact"] = contact

def privacy(lang):
    if lang == "es":
        h = page_hero("Legal", "Política de Privacidad")
        secs = [
            (None, "Esta política explica cómo AREX Mining S.A. recolecta, utiliza, comunica y protege los datos personales, de conformidad con la Ley N.º 25.326 de Protección de los Datos Personales de la República Argentina y su normativa reglamentaria. Se aplica a este sitio web y a las consultas enviadas a través de él."),
            ("Quiénes somos", 'Este sitio web es operado por AREX MINING S.A. (“AREX Mining”, “nosotros”), sociedad constituida en la República Argentina. <span class="draft" style="display:block">Completar CUIT y domicilio legal.</span>'),
            ("Qué datos recolectamos", "Recolectamos únicamente los datos personales que usted decide proporcionarnos a través del formulario de consulta: su nombre, cargo, empresa y correo electrónico, junto con la información incluida en su mensaje. No recolectamos datos personales de forma pasiva, y este sitio no utiliza cookies ni tecnologías de seguimiento."),
            ("Para qué los utilizamos", "Utilizamos los datos personales exclusivamente para responder a su consulta, comunicarnos con usted al respecto y llevar un registro de la correspondencia. No los utilizamos con fines publicitarios sin su consentimiento específico, y no vendemos ni cedemos datos personales a terceros."),
            ("Consentimiento", "Al enviar el formulario de consulta, usted presta su consentimiento libre, expreso e informado para que recolectemos y utilicemos sus datos personales con las finalidades descriptas. Puede revocar su consentimiento en cualquier momento contactándonos; la revocación puede impedir que respondamos una consulta pendiente."),
            ("Comunicación de datos", "Podemos comunicar datos personales a las empresas para las que desarrollamos proyectos, como AREX Copper y 3C Resources, cuando sea necesario para responder a su consulta, y a proveedores de servicios que actúan por nuestra cuenta. Las consultas enviadas a través de este sitio se transmiten mediante un servicio de formularios de terceros. También podemos comunicar datos cuando lo exija la ley o una autoridad competente."),
            ("Transferencias internacionales", "Los datos personales pueden ser transferidos y tratados en otros países donde nosotros, las empresas para las que trabajamos o nuestros proveedores operamos, incluida la República de Singapur. En esos casos adoptamos medidas para que los datos reciban un nivel de protección adecuado, conforme a la normativa argentina."),
            ("Seguridad", "Aplicamos medidas técnicas y organizativas razonables para proteger los datos personales contra el acceso, uso o divulgación no autorizados. Este sitio se sirve mediante una conexión cifrada. Ningún método de transmisión por internet es completamente seguro, y no podemos garantizar una seguridad absoluta."),
            ("Conservación", "Conservamos los datos personales solo durante el tiempo necesario para la finalidad para la que fueron recolectados, o según lo exijan obligaciones legales, y luego los eliminamos o anonimizamos."),
            ("Sus derechos", "Usted puede solicitar el acceso, la rectificación, la actualización y la supresión de sus datos personales. Responderemos las solicitudes de acceso dentro de los diez días corridos y las de rectificación, actualización o supresión dentro de los cinco días hábiles, conforme a la Ley N.º 25.326."),
            (None, "El titular de los datos personales tiene la facultad de ejercer el derecho de acceso a los mismos en forma gratuita a intervalos no inferiores a seis meses, salvo que se acredite un interés legítimo al efecto conforme lo establecido en el artículo 14, inciso 3 de la Ley N.º 25.326. La Agencia de Acceso a la Información Pública, en su carácter de Órgano de Control de la Ley N.º 25.326, tiene la atribución de atender las denuncias y reclamos que interpongan quienes resulten afectados en sus derechos por incumplimiento de las normas vigentes en materia de protección de datos personales."),
            ("Contacto", 'Las consultas, solicitudes y reclamos relativos a datos personales deben dirigirse a AREX Mining. <span class="draft" style="display:block">Completar correo electrónico y domicilio para consultas sobre privacidad.</span>'),
            ("Cambios en esta política", "Podemos actualizar esta política periódicamente. La versión vigente se publica siempre en esta página, con la fecha de su última actualización."),
        ]
        date = "Última actualización: 4 de noviembre de 2026"
    else:
        h = page_hero("Legal", "Privacy Policy")
        secs = [
            (None, "This policy explains how AREX Mining S.A. collects, uses, discloses and protects personal data in accordance with Argentina's Personal Data Protection Law No. 25,326 and its regulations. It applies to this website and to enquiries submitted through it."),
            ("Who we are", 'This website is operated by AREX MINING S.A. (“AREX Mining”, “we”, “us”), a company incorporated in the Argentine Republic. <span class="draft" style="display:block">Add CUIT and registered address.</span>'),
            ("What we collect", "We collect only the personal data you choose to provide through our enquiry form: your name, position, company and email address, together with any information contained in your message. We do not collect personal data passively, and this website does not use cookies or tracking technologies."),
            ("Why we collect it", "We use personal data solely to respond to your enquiry, to communicate with you about it, and to keep a record of correspondence. We do not use it for marketing without your specific consent, and we do not sell or transfer personal data to third parties."),
            ("Consent", "By submitting the enquiry form you give your free, express and informed consent to our collecting and using your personal data for the purposes described. You may withdraw consent at any time by contacting us; withdrawal may mean we can no longer respond to an outstanding enquiry."),
            ("Disclosure", "We may disclose personal data to the companies for which we develop projects, such as AREX Copper and 3C Resources, where necessary to respond to your enquiry, and to service providers acting on our behalf. Enquiries submitted through this website are transmitted by a third-party form service. We may also disclose personal data where required by law or by a competent authority."),
            ("International transfers", "Personal data may be transferred to and processed in other countries where we, the companies we work for or our service providers operate, including the Republic of Singapore. In those cases we take steps to ensure the data receives an adequate level of protection under Argentine law."),
            ("Security", "We apply reasonable technical and organisational measures to protect personal data against unauthorised access, use or disclosure. This website is served over an encrypted connection. No method of transmission over the internet is entirely secure, and we cannot guarantee absolute security."),
            ("Retention", "We retain personal data only for as long as it is needed for the purpose for which it was collected, or as required by law, after which it is deleted or anonymised."),
            ("Your rights", "You may request access to, correction, updating and deletion of your personal data. We will respond to access requests within ten calendar days and to correction, updating or deletion requests within five business days, as provided by Law No. 25,326."),
            (None, "Data subjects may exercise the right of access to their personal data free of charge at intervals of no less than six months, unless a legitimate interest is shown, as provided in section 14(3) of Law No. 25,326. The Agency for Access to Public Information (Agencia de Acceso a la Información Pública), as the supervisory authority under Law No. 25,326, is empowered to handle complaints from anyone whose rights are affected by non-compliance with data protection rules."),
            ("Contact", 'Questions, requests and complaints about personal data should be directed to AREX Mining. <span class="draft" style="display:block">Add email and postal address for privacy enquiries.</span>'),
            ("Changes to this policy", "We may update this policy from time to time. The current version is always published on this page, with the date of the most recent update shown above."),
        ]
        date = "Last updated: 4 November 2026"
    lede = secs[0][1]
    rest = "".join((f"<h2>{t}</h2><p>{p}</p>" if t else f"<p>{p}</p>") for t, p in secs[1:])
    body = h + f'<section><div class="wrap narrow legal-doc"><p class="lede">{lede}</p><p class="doc-date">{date}</p>{rest}</div></section>'
    t = "Política de Privacidad — AREX Mining" if lang == "es" else "Privacy Policy — AREX Mining"
    d = ("Política de privacidad de AREX Mining S.A., conforme a la Ley N.º 25.326." if lang == "es"
         else "AREX Mining S.A. privacy policy under Argentina's Law No. 25,326.")
    return t, d, body
PAGES["privacy"] = privacy

# ---------------------------------------------------------------- write
os.makedirs(OUT, exist_ok=True)
count = 0
for slug, fn in PAGES.items():
    for lang in LANGS:
        title, desc, body = fn(lang)
        with open(os.path.join(OUT, href(slug, lang)), "w", encoding="utf-8") as fh:
            html = page(lang, slug, title, desc, body)
            fh.write(to_lang(html, lang) if lang in TABLES else html)
        count += 1
print("pages:", count)
for _l, _m in MISSING.items():
    json.dump(sorted(_m), open(os.path.join(HERE, f"{_l}_missing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(_l, "missing:", len(_m))
