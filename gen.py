#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las 7 páginas del sitio de Nadina's Spa desde una plantilla común."""
import os, re, json, pathlib

RAIZ = pathlib.Path("/home/claude/w2")

# fuente única: los servicios salen de datos.js, volcados por node a servicios.json
TEN = {"servicios": json.loads((RAIZ/"servicios.json").read_text(encoding="utf-8"))}

CATS = [
    ("laser",            "Depilación láser"),
    ("faciales",         "Faciales"),
    ("corporales",       "Corporales"),
    ("day-spa",          "Nadina's Day Spa"),
    ("peeling",          "Peeling"),
    ("rejuvenecimiento", "Rejuvenecimiento"),
]

SILUETA = '''<svg viewBox="0 0 260 600" role="img" aria-label="Silueta con las zonas de tratamiento">
            <defs>
              <clipPath id="cp-d"><ellipse cx="130" cy="42" rx="25" ry="30"/>
                <path id="mit-d" d="M130,74 L116,78 C103,82 91,90 86,106 C78,132 70,176 66,216 C63,240 61,258 61,272 L82,274 C84,250 87,214 90,180 C93,156 96,142 98,134 C100,162 103,200 104,232 C101,260 91,280 85,304 C83,336 86,368 89,400 C92,438 94,456 97,486 C99,520 101,552 103,578 L120,578 C119,545 118,505 117,468 C116,430 119,398 126,366 L130,348 Z"/>
                <use href="#mit-d" transform="translate(260,0) scale(-1,1)"/></clipPath>
              <clipPath id="cp-c"><ellipse cx="130" cy="42" rx="26" ry="30"/>
                <path id="mit-c" d="M130,72 L112,76 C96,80 81,88 75,106 C67,132 60,176 56,216 C53,240 51,258 51,272 L73,274 C75,250 79,214 82,180 C85,156 89,140 92,132 C94,160 96,196 96,226 C95,252 90,278 88,302 C86,334 89,366 92,398 C95,436 97,454 100,484 C102,518 104,552 106,578 L122,578 C121,545 120,505 119,468 C118,430 120,398 126,366 L130,348 Z"/>
                <use href="#mit-c" transform="translate(260,0) scale(-1,1)"/></clipPath>
            </defs>
            <g id="figura" clip-path="url(#cp-d)">
              <rect x="0" y="0" width="260" height="600" class="silueta"/>
              <g id="zonas"></g>
            </g>
          </svg>'''


def cabeza(titulo, desc, base, extra_css=""):
    return f'''<!DOCTYPE html>
<html lang="es-VE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#EAF1EE">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{base}assets/logo/favicon.ico">
<link rel="apple-touch-icon" href="{base}assets/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..500&family=Jost:wght@300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/estilo.css">{extra_css}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "Nadina's Spa",
  "legalName": "NADINASSPA, C.A",
  "taxID": "J-50699892-0",
  "url": "https://www.nadinasspa.com/",
  "telephone": "+584129395252",
  "email": "contacto@nadinasspa.com",
  "image": "https://www.nadinasspa.com/assets/img/hero-recepcion.webp",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Av. Macaracuay, C.C. Multicentro Macaracuay, Nivel 5, Oficina 5",
    "addressLocality": "Caracas",
    "addressRegion": "Miranda",
    "postalCode": "1071",
    "addressCountry": "VE"
  }},
  "geo": {{ "@type": "GeoCoordinates", "latitude": 10.4672212, "longitude": -66.8170936 }},
  "hasMap": "https://maps.app.goo.gl/RpD2WbL8R8R6A8N59",
  "sameAs": ["https://instagram.com/nadinasspa"],
  "openingHoursSpecification": [
    {{ "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00", "closes": "18:00" }},
    {{ "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday", "opens": "10:00", "closes": "14:00" }}
  ],
  "priceRange": "$$"
}}
</script>

</head>
<body data-base="{base}">'''


def nav(base, activo=None):
    enl = "".join(
        f'      <a href="{base}{s}/"{" aria-current=\"page\"" if s==activo else ""}>{n}</a>\n'
        for s, n in CATS[:4]
    )
    return f'''
<header class="nav">
  <div class="nav__in">
    <a href="{base}index.html" aria-label="Nadina's Spa, inicio"><img class="nav__logo" src="{base}assets/logo/logotipo-tinta.png" alt="Nadina's Spa"></a>
    <nav class="nav__links" aria-label="Categorías">
{enl}    </nav>
    <a class="btn js-wa" data-msg="Hola, quiero reservar una cita." data-tok="NAV">Escríbenos</a>
  </div>
</header>
'''


def contacto(base):
    return f'''
<section class="res" id="reservar">
  <div class="env">
    <p class="eyebrow">Reservar</p>
    <h2>Escríbenos y <em>te confirmamos</em> hoy.</h2>
    <p>Cuéntanos qué te interesa y te damos precios, disponibilidad y todo lo que necesites saber antes de venir.</p>
    <a class="wa-marca js-wa" data-msg="Hola, quiero reservar una cita en Nadina's Spa." data-tok="PIE">
      <img class="wa-marca__logo" src="{base}assets/logo/whatsapp.svg" alt="WhatsApp" width="38" height="38">
      <span class="wa-marca__txt">Escríbenos</span>
    </a>

    <div class="datos">
      <div>
        <span class="eyebrow">Dónde estamos</span>
        <p>Av. Macaracuay, C.C. Multicentro Macaracuay<br>Nivel 5, Oficina 5<br>Urb. Macaracuay, Caracas, Miranda 1071<br>
        <a href="https://maps.app.goo.gl/RpD2WbL8R8R6A8N59" target="_blank" rel="noopener">Cómo llegar</a></p>
      </div>
      <div>
        <span class="eyebrow">Horario</span>
        <p>Lunes a viernes · 9:00 – 18:00<br>Sábados · 10:00 – 14:00<br>Domingos cerrado</p>
      </div>
      <div>
        <span class="eyebrow">Contacto</span>
        <p><a class="js-wa" data-msg="Hola, tengo una consulta." data-tok="TEL">+58 412 939 5252</a><br>
        <a href="mailto:contacto@nadinasspa.com">contacto@nadinasspa.com</a><br>
        <a href="https://instagram.com/nadinasspa" target="_blank" rel="noopener">@nadinasspa</a></p>
      </div>
    </div>

    <div class="pie">
      <img src="{base}assets/logo/logotipo-oro.png" alt="Nadina's Spa">
      <span>© <span id="anio"></span> NADINASSPA, C.A · RIF J-50699892-0 · Caracas, Venezuela</span>
      <a href="{base}privacidad/">Política de privacidad</a>
    </div>
  </div>
</section>

<a class="flota js-wa" data-msg="Hola, quiero reservar una cita en Nadina's Spa." data-tok="FLOT" aria-label="Escríbenos por WhatsApp">
  <img src="{base}assets/logo/whatsapp.svg" alt="WhatsApp" width="56" height="56">
</a>

<script src="{base}assets/js/datos.js"></script>
<script src="{base}assets/js/comun.js"></script>'''


def otras(base, actual):
    items = "".join(
        f'      <a href="{base}{s}/">{n}</a>\n' for s, n in CATS if s != actual
    )
    return f'''
<section class="franja franja--papel">
  <div class="env">
    <p class="eyebrow">Seguir viendo</p>
    <h2>Otras cosas que hacemos.</h2>
    <div class="otras">
{items}    </div>
  </div>
</section>
'''


def servicios_html(lista):
    filas = []
    for s in lista:
        u = f'<span class="serv__u">{s["u"]}</span>' if s.get("u") else ""
        d = f'<p class="serv__d">{s["d"]}</p>' if s.get("d") else ""
        filas.append(
            f'      <div class="serv rev"><span class="serv__b"></span>'
            f'<div><span class="serv__n">{s["n"]}</span>{d}{u}</div></div>\n'
        )
    return '    <div class="servs">\n' + "".join(filas) + "    </div>\n"


def aviso_precio(tok, texto="Los precios y la disponibilidad te los damos por WhatsApp, con el detalle de tu caso."):
    return (f'    <p class="aviso"><b>¿Cuánto cuesta?</b> {texto} '
            f'<a class="js-wa" data-msg="Hola, quiero consultar precios y disponibilidad." data-tok="{tok}">'
            f'Escríbenos y te respondemos</a>.</p>\n')


def conf_html(set_, titulo, sub, boton):
    return f'''
<section class="franja" id="configurador">
  <div class="env">
    <p class="eyebrow">Arma tu tratamiento</p>
    <h2>{titulo}</h2>
    <p class="franja__sub">{sub}</p>

    <div id="conf" data-set="{set_}">
      <div class="mandos">
        <div class="seg" role="group" aria-label="Género">
          <button data-g="damas" aria-pressed="true">Damas</button>
          <button data-g="caballeros" aria-pressed="false">Caballeros</button>
        </div>
        <div class="seg" role="group" aria-label="Vista del cuerpo">
          <button data-v="frente" aria-pressed="true">Frente</button>
          <button data-v="espalda" aria-pressed="false">Espalda</button>
        </div>
      </div>

      <div class="conf__grid">
        <div class="cuerpo">
          {SILUETA}
          <p class="pista" id="pista">Toca una zona</p>
        </div>
        <div class="lado">
          <div class="chips" id="chips"></div>
          <div class="cesta">
            <h3>Tus zonas</h3>
            <p class="cesta__v" id="vacia">Aún no has elegido ninguna. Toca el cuerpo o la lista de arriba.</p>
            <ul id="items"></ul>
            <div class="acciones" id="acciones" hidden>
              <a class="btn btn--lg js-cotiza">{boton}</a>
            </div>
            <p class="legal">Te respondemos con el precio de cada zona, los combos que apliquen y las opciones de pago: sesión por sesión o paquete adelantado.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# ═══════════════════════════════════════════════════════════════════════════
#  PORTADA
# ═══════════════════════════════════════════════════════════════════════════
def portada():
    tarjetas = []
    for i, (slug, nombre) in enumerate(CATS):
        cls = "tarj--ancha" if i == 0 else "tarj--med"
        img = {"laser":"cat-laser","faciales":"cat-faciales","corporales":"cat-corporales",
               "day-spa":"cat-dayspa","peeling":"cat-peeling","rejuvenecimiento":"cat-rejuvenecimiento"}[slug]
        txt = {
            "laser":"Alma Soprano Titanium, tres longitudes de onda a la vez. 26 zonas para damas y caballeros, con valoración antes de empezar.",
            "faciales":"Limpiezas profundas, exosomas y nutrición",
            "corporales":"Masajes, reductores y moldeado",
            "day-spa":"Cumpleaños, aniversarios y días de relax",
            "peeling":"Renovación celular por zona",
            "rejuvenecimiento":"Bótox, ácido hialurónico, PDRN",
        }[slug]
        tarjetas.append(
            f'      <a class="tarj {cls}" href="{slug}/">\n'
            f'        <div class="tarj__f"><img data-medio="{img}" alt="{nombre} en Nadina\'s Spa" loading="lazy" width="900" height="675"></div>\n'
            f'        <div class="tarj__p"><h3>{nombre}</h3><p>{txt}</p></div>\n'
            f'      </a>\n')

    return (cabeza("Nadina's Spa · Centro estético y depilación láser en Caracas",
                   "Centro estético en Macaracuay, Caracas. Depilación láser con Alma Soprano Titanium, faciales, corporales, day spa y rejuvenecimiento.",
                   "")
    + nav("")
    + f'''
<main>
<section class="hero">
  <div class="hero__aura" aria-hidden="true"><i></i><i></i></div>
  <div class="env hero__in">
    <div>
      <p class="eyebrow">Centro estético · Macaracuay, Caracas</p>
      <h1>Tu piel, con <em>tiempo</em> y criterio.</h1>
      <p class="hero__p">Depilación láser con Alma Soprano Titanium, medicina estética y faciales. Un equipo corto que evalúa antes de tratar y te dice la verdad sobre lo que necesitas.</p>
      <div class="hero__cta">
        <a class="btn btn--lg" href="#servicios">Ver qué hacemos</a>
        <a class="btn btn--g btn--lg js-wa" data-msg="Hola, quiero reservar una cita." data-tok="HERO">Escríbenos</a>
      </div>
    </div>
    <div class="marco"><span>Aquí va el video del centro</span></div>
  </div>
</section>

<section class="puerta" id="servicios">
  <div class="env">
    <div class="puerta__cab">
      <p class="eyebrow">Qué hacemos</p>
      <h2>Seis formas de cuidarte.</h2>
      <p>Elige por dónde quieres empezar. Cada una tiene su propia página con el detalle.</p>
    </div>
    <div class="rej">
{"".join(tarjetas)}    </div>
  </div>
</section>

<section class="franja franja--menta">
  <div class="env duo">
    <div>
      <p class="eyebrow">La tecnología</p>
      <h2>Trabajamos con Alma Soprano Titanium.</h2>
      <p>Es el equipo de referencia en depilación láser. Combina tres longitudes de onda —755, 810 y 1064 nanómetros— emitidas al mismo tiempo, que alcanzan distintas profundidades del folículo en un solo disparo.</p>
      <p>Su sistema de enfriamiento continuo y la punta de zafiro mantienen la piel fría mientras el calor trabaja donde tiene que trabajar. Por eso es apto para todos los tonos de piel y la sesión resulta cómoda.</p>
      <p style="color:var(--tinta-3);font-size:.88rem">Puedes buscarlo. Preferimos que sepas exactamente con qué te vamos a tratar.</p>
    </div>
    <div>
      <div class="foto foto--v"><img data-medio="equipo-soprano" alt="Equipo Alma Soprano Titanium en la sala de láser" loading="lazy" width="900" height="1125"></div>
      <p class="pie-foto">Sala de láser · Nadina's Spa, Macaracuay</p>
    </div>
  </div>
</section>

<section class="franja">
  <div class="env">
    <div class="puerta__cab">
      <p class="eyebrow">Cómo trabajamos</p>
      <h2>Cuatro cosas que no negociamos.</h2>
      <p>No son valores de folleto. Son las reglas por las que a veces perdemos una venta.</p>
    </div>
    <div class="credo__lista">
      <div class="credo__it rev"><h3>Diagnóstico antes que catálogo</h3>
        <p>Cada tratamiento empieza evaluando tu piel, no eligiendo de una lista. Lo que le sirve a tu amiga puede no servirte a ti, y en estética eso no es un detalle.</p></div>
      <div class="credo__it rev"><h3>Tecnología que entendemos</h3>
        <p>No compramos aparatos por moda ni aplicamos protocolos que no sepamos explicar. Si preguntas por qué usamos algo, te lo contamos.</p></div>
      <div class="credo__it rev"><h3>Te decimos cuántas sesiones</h3>
        <p>Con un rango honesto desde la primera valoración y las opciones de pago sobre la mesa. Nadie debería enterarse a mitad de camino de que faltan seis sesiones más.</p></div>
      <div class="credo__it rev"><h3>Sin promesas que no podamos sostener</h3>
        <p>Si un tratamiento no va a funcionar en tu caso, te lo decimos antes de cobrarlo. Preferimos perder una venta que un resultado.</p></div>
    </div>
  </div>
</section>


<section class="franja franja--papel" id="fundadora">
  <div class="env duo">
    <div>
      <p class="eyebrow">Quién está detrás</p>
      <h2>Nadina Lastra, fundadora.</h2>
      <p>El centro lleva su segundo nombre, y eso no es casualidad: la persona que revisa tu piel es la misma que va a trabajarla, y la que te dice cuántas sesiones vas a necesitar de verdad.</p>
      <p>Acá no hay un mostrador que vende y un fondo que ejecuta. Si un tratamiento no es para ti, te lo decimos antes de cobrarlo.</p>
      <span class="firma-f">— texto pendiente de la sesión de fotos</span>
    </div>
    <div>
      <div class="foto foto--v" id="foto-fundadora">
        <div class="hueco"><span>Retrato de Nadina &middot; toma D1 del brief</span></div>
      </div>
    </div>
  </div>
</section>

<section class="franja">
  <div class="env duo duo--inv">
    <div>
      <div class="foto"><img data-medio="giftcards" alt="Gift Cards de Nadina's Spa" loading="lazy" width="900" height="675"></div>
    </div>
    <div>
      <p class="eyebrow">Para regalar</p>
      <h2>Gift Cards.</h2>
      <p>Un tratamiento es un regalo que se disfruta el día que se usa y se recuerda semanas después. Tenemos tarjetas para cualquier ocasión: cumpleaños, aniversarios, el Día de las Madres, o sin motivo.</p>
      <p>Tú eliges el monto o el tratamiento, nosotros preparamos la tarjeta. Se puede entregar en el centro o enviarla en digital.</p>
      <p><a class="btn js-wa" data-msg="Hola, quiero regalar una Gift Card." data-tok="GIFT">Pedir una Gift Card</a></p>
    </div>
  </div>
</section>

<section class="frase">
  <div class="env">
    <blockquote>Si crees que puedes, ya estás a medio camino.</blockquote>
    <cite>En la pared de nuestro centro</cite>
  </div>
</section>

<section class="franja franja--menta">
  <div class="env">
    <p class="eyebrow">Tu visita</p>
    <h2>Antes de venir.</h2>
    <div class="malla">
      <div class="rev"><h3>Solo con cita previa</h3><p>Lunes a viernes de 9:00 a 18:00 y sábados de 10:00 a 14:00. Domingos cerrado.</p></div>
      <div class="rev"><h3>Los inyectables tienen jornada</h3><p>Bótox y rellenos, miércoles y viernes. Plasma rico en plaquetas, lunes y miércoles. Se agendan aparte.</p></div>
      <div class="rev"><h3>El Day Spa necesita aviso</h3><p>La cabina se prepara solo para ustedes, con decoración y detalle incluidos. Resérvalo con días de anticipación.</p></div>
      <div class="rev"><h3>Cuéntanos tu historial</h3><p>Embarazo, lactancia, medicación fotosensible, alergias o un tratamiento reciente. Cambia lo que podemos aplicar.</p></div>
    </div>
  </div>
</section>
</main>
'''
    + contacto("") + "\n</body>\n</html>\n")


# ═══════════════════════════════════════════════════════════════════════════
#  PÁGINAS DE CATEGORÍA
# ═══════════════════════════════════════════════════════════════════════════
def pagina(slug, nombre, eyebrow, h1, intro, cuerpo, desc, conf=False):
    b = "../"
    extra = f'\n<script defer src="{b}assets/js/configurador.js"></script>' if conf else ""
    return (cabeza(f"{nombre} · Nadina's Spa", desc, b)
    + nav(b, slug)
    + f'''
<main>
<div class="env migas"><a href="{b}index.html">Inicio</a> · {nombre}</div>

<section class="franja" style="padding-top:clamp(24px,4vw,44px)">
  <div class="env">
    <p class="eyebrow">{eyebrow}</p>
    <h2 style="font-size:clamp(2.1rem,5.4vw,3.6rem);max-width:16ch">{h1}</h2>
    <p class="franja__sub" style="font-size:1.03rem">{intro}</p>
  </div>
</section>
'''
    + cuerpo
    + otras(b, slug)
    + '</main>\n'
    + contacto(b)
    + (f'\n<script defer src="{b}assets/js/configurador.js"></script>' if conf else "")
    + "\n</body>\n</html>\n")


def escribir(ruta, contenido):
    p = RAIZ / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    return len(contenido)





# ═══════════════════════════════════════════════════════════════════════════
#  CONTENIDO DE CADA CATEGORÍA
# ═══════════════════════════════════════════════════════════════════════════
def foto_ancha(img, alt, pie=""):
    p = f'    <p class="pie-foto">{pie}</p>\n' if pie else ""
    return (f'<section class="franja" style="padding-top:0">\n  <div class="env">\n'
            f'    <div class="foto"><img data-medio="{img}" alt="{alt}" loading="lazy" width="1400" height="875"></div>\n'
            f'{p}  </div>\n</section>\n')


def pagina_laser():
    pasos = [
        ("01","Valoración","Miramos tu piel y tu vello antes de tocar el equipo, y ahí te decimos cuántas sesiones vas a necesitar de verdad. Si el láser no es para tu caso, te lo decimos ahí mismo."),
        ("02","Cuéntanos tu historial","Embarazo, lactancia, medicación fotosensible o tatuajes en la zona. Todo eso cambia lo que podemos aplicar y con qué intensidad."),
        ("03","Aféitate un día antes","Rasura con afeitadora el día previo o el mismo día. Nada que arranque de raíz: ni cera ni pinza. Sin la raíz en su sitio, el láser no tiene a qué apuntar."),
        ("04","La sesión","El calor sube de forma progresiva mientras el cabezal se mueve, y la piel se enfría todo el tiempo. Sales y sigues con tu día."),
        ("05","Vuelves entre 21 y 30 días después","Mínimo tres semanas, máximo un mes. Antes no sirve porque el folículo no está listo; después se pierde el ritmo de la serie."),
        ("06","Entre 8 y 12 sesiones","Aclara la zona, elimina la foliculitis y mejora la textura de la piel. Se nota desde la primera, pero el resultado completo llega al terminar la serie."),
    ]
    ps = "".join(f'      <div class="paso rev"><span class="paso__n">{n}</span><div><h3>{t}</h3><p>{d}</p></div></div>\n'
                 for n,t,d in pasos)
    cuerpo = f'''
<section class="franja franja--menta" style="padding-top:clamp(30px,5vw,60px)">
  <div class="env duo">
    <div>
      <p class="eyebrow">La tecnología</p>
      <h2>Alma Soprano Titanium.</h2>
      <p>Es el equipo de referencia del sector, y fue el primero en combinar tres longitudes de onda emitidas al mismo tiempo: 755, 810 y 1064 nanómetros. Cada una alcanza una profundidad distinta del folículo, así que un solo disparo trabaja el tallo, la raíz y la base.</p>
      <p>El cabezal enfría la piel de forma continua con una punta de zafiro: el frío se queda en la superficie y el calor trabaja abajo. Por eso la sesión es cómoda y por eso funciona en todos los tonos de piel, no solo en las claras.</p>
      <p style="color:var(--tinta-3);font-size:.88rem">Búscalo si quieres. Preferimos que sepas con qué te vamos a tratar.</p>
    </div>
    <div>
      <div class="foto foto--v"><img data-medio="equipo-soprano" alt="Alma Soprano Titanium" loading="lazy" width="900" height="1125"></div>
      <p class="pie-foto">El equipo, en nuestra sala de láser</p>
    </div>
  </div>
</section>

<section class="franja">
  <div class="env">
    <p class="eyebrow">Cómo funciona</p>
    <h2>De la primera consulta a la última sesión.</h2>
    <p class="franja__sub">Esto aplica igual para damas y caballeros, y para cualquier zona.</p>
    <div class="pasos">
{ps}    </div>
  </div>
</section>

{foto_ancha("sala-laser","Sala de depilación láser de Nadina's Spa","Nuestra sala de láser, en Macaracuay")}
''' + conf_html("laser",
        "Elige tus zonas y te pasamos el presupuesto.",
        "Toca en el cuerpo o en la lista. Al terminar, el mensaje llega a WhatsApp con tu selección ya escrita: no tienes que explicar nada.",
        "Pedir mi presupuesto") + f'''
<section class="franja franja--papel">
  <div class="env">
    <p class="eyebrow">Formas de pagarlo</p>
    <h2>Tú decides el ritmo.</h2>
    <p class="franja__sub">Son mínimo ocho sesiones, así que la idea no es que pagues todo de una vez.</p>
    <div class="servs">
      <div class="serv rev"><span class="serv__b"></span><div><span class="serv__n">Sesión por sesión</span>
        <p class="serv__d">Pagas cada vez que vienes. Sin compromiso de serie: puedes empezar y decidir sobre la marcha.</p></div></div>
      <div class="serv rev"><span class="serv__b"></span><div><span class="serv__n">Combos del mismo día</span>
        <p class="serv__d">Varias zonas juntas en una sola visita, a mejor precio que por separado. Te decimos cuál aplica según lo que elijas.</p></div></div>
      <div class="serv rev"><span class="serv__b"></span><div><span class="serv__n">Paquete de 6 sesiones</span>
        <p class="serv__d">Pago adelantado. Sale mejor por sesión y cubre la mayor parte de la serie recomendada.</p></div></div>
      <div class="serv rev"><span class="serv__b"></span><div><span class="serv__n">Paquetes de 4 sesiones, con zona de obsequio</span>
        <p class="serv__d">Combinaciones ya armadas de varias zonas. Incluyen sesiones de una zona pequeña sin cobro adicional.</p>
        <span class="serv__u">Con obsequio</span></div></div>
    </div>
''' + aviso_precio("LSRP") + '''  </div>
</section>
'''
    return pagina("laser","Depilación láser","Depilación láser",
        "El vello no vuelve, y la piel queda mejor de lo que estaba.",
        "Trabajamos con Alma Soprano Titanium, apto para todos los tonos de piel. Arma tu tratamiento abajo y te pasamos el presupuesto por WhatsApp.",
        cuerpo,
        "Depilación láser en Caracas con Alma Soprano Titanium. 26 zonas para damas y caballeros, en Macaracuay.",
        conf=True)


def pagina_faciales():
    cuerpo = f'''
{foto_ancha("sala-faciales","Cabina de faciales de Nadina's Spa","Nuestra cabina de faciales y corporales")}

<section class="franja franja--menta">
  <div class="env">
    <p class="eyebrow">Qué incluye</p>
    <h2>Cada limpieza empieza con un diagnóstico.</h2>
    <p class="franja__sub">El protocolo se ajusta a lo que encontremos en tu piel, no al revés. Por eso dos limpiezas del mismo nombre no son iguales.</p>
''' + servicios_html(TEN["servicios"]["faciales"]) + aviso_precio("FAC") + '''  </div>
</section>

<section class="franja">
  <div class="env">
    <p class="eyebrow">La limpieza profunda, paso a paso</p>
    <h2>Once pasos en una sola sesión.</h2>
    <div class="pasos">
      <div class="paso rev"><span class="paso__n">01</span><div><h3>Diagnóstico</h3><p>Miramos tu piel de cerca antes de decidir qué usar.</p></div></div>
      <div class="paso rev"><span class="paso__n">02</span><div><h3>Higienización y exfoliación</h3><p>Retiramos maquillaje, impurezas y células muertas.</p></div></div>
      <div class="paso rev"><span class="paso__n">03</span><div><h3>Vapor ozono</h3><p>Abre el poro y prepara la piel para la extracción.</p></div></div>
      <div class="paso rev"><span class="paso__n">04</span><div><h3>Extracción</h3><p>La parte que más se nota. Con criterio, sin maltratar la piel.</p></div></div>
      <div class="paso rev"><span class="paso__n">05</span><div><h3>Paleta ultrasónica y alta frecuencia</h3><p>Limpieza profunda y control bacteriano.</p></div></div>
      <div class="paso rev"><span class="paso__n">06</span><div><h3>Martillo frío y mascarilla</h3><p>Descongestiona, cierra el poro y calma.</p></div></div>
      <div class="paso rev"><span class="paso__n">07</span><div><h3>Máscara led e hidratación</h3><p>Según lo que necesite tu piel ese día.</p></div></div>
      <div class="paso rev"><span class="paso__n">08</span><div><h3>Protector solar</h3><p>Sales protegida. Después de una limpieza no es opcional.</p></div></div>
    </div>
  </div>
</section>
'''
    return pagina("faciales","Faciales","Faciales",
        "Tu piel, leída antes de ser tratada.",
        "Limpiezas profundas, hidradermoabrasión y nutrición. Empezamos mirando qué tiene tu piel y de ahí sale el protocolo.",
        cuerpo, "Limpiezas faciales profundas e hidrafacial en Caracas. Centro estético en Macaracuay.")


def pagina_corporales():
    cuerpo = f'''
{foto_ancha("sala-masajes","Sala de masajes de Nadina's Spa","Nuestra sala de masajes")}

<section class="franja franja--menta">
  <div class="env">
''' + '    <p class="eyebrow">Qué hacemos</p>\n    <h2>Reductores en serie, masajes por sesión.</h2>\n' + \
'    <p class="franja__sub">Los packs reductores se trabajan en cinco sesiones porque el resultado depende de completarlas. Los masajes son sueltos: vienes cuando lo necesitas.</p>\n' + \
servicios_html(TEN["servicios"]["corporales"]) + aviso_precio("COR") + '''  </div>
</section>

<section class="franja">
  <div class="env duo">
    <div>
      <p class="eyebrow">Los packs reductores</p>
      <h2>Cinco sesiones, y lo decimos desde el principio.</h2>
      <p>Una sesión suelta de reductor no hace nada duradero. El plan es de cinco, con maderoterapia o con aparatología según tu caso, y así lo planteamos desde la primera consulta.</p>
      <p>Combinamos técnicas en cada sesión: radiofrecuencia, drenaje linfático, lipoláser o ultracavitación. Cada pack incluye papel reductor osmótico.</p>
      <p>Si buscas un resultado en una sola sesión, te vamos a decir que no existe. Preferimos eso a que te vayas decepcionada en la tercera.</p>
    </div>
    <div>
      <div class="foto foto--v"><img data-medio="cat-corporales" alt="Cabina de tratamientos corporales" loading="lazy" width="900" height="675"></div>
    </div>
  </div>
</section>
'''
    return pagina("corporales","Corporales","Corporales y masajes",
        "Para soltar tensión, o para moldear.",
        "Masajes relajantes y descontracturantes por sesión, y packs reductores de cinco sesiones con aparatología.",
        cuerpo, "Masajes y tratamientos corporales reductores en Caracas. Centro estético en Macaracuay.")


def pagina_dayspa():
    cuerpo = f'''
{foto_ancha("dayspa-cabina","Cabina decorada para Nadina's Day Spa","Cabina preparada para un Day Spa")}

<section class="franja franja--menta">
  <div class="env">
    <p class="eyebrow">Las cuatro opciones</p>
    <h2>Sola o acompañada, estándar o premium.</h2>
    <p class="franja__sub">La cabina se prepara solo para ustedes. Por eso hace falta reservar con días de anticipación.</p>
''' + servicios_html(TEN["servicios"]["day-spa"]) + aviso_precio("DAY") + '''  </div>
</section>

<section class="franja">
  <div class="env duo duo--inv">
    <div>
      <div class="foto"><img data-medio="giftcards" alt="Gift Cards de Nadina's Spa" loading="lazy" width="900" height="675"></div>
    </div>
    <div>
      <p class="eyebrow">Para regalar</p>
      <h2>El Day Spa es el regalo que más nos piden.</h2>
      <p>Cumpleaños, aniversarios, el Día de las Madres, o simplemente porque alguien lo necesitaba. Preparamos la Gift Card con el tratamiento que elijas y la entregamos en el centro o en digital.</p>
      <p><a class="btn js-wa" data-msg="Hola, quiero regalar un Day Spa." data-tok="GIFT">Pedir una Gift Card</a></p>
    </div>
  </div>
</section>
'''
    return pagina("day-spa","Nadina's Day Spa","Nadina's Day Spa",
        "Un día entero dedicado a no hacer nada.",
        "Limpieza facial con ácido hialurónico y oro de 24 quilates, masaje con aceites aromáticos, musicoterapia y aromaterapia. En la versión premium, decoración de cabina, flores o chocolate y una copa.",
        cuerpo, "Day Spa en Caracas para cumpleaños y aniversarios. Paquetes individuales y para dos personas.")


def pagina_peeling():
    cuerpo = '''
<section class="franja franja--menta" style="padding-top:clamp(30px,5vw,60px)">
  <div class="env">
    <p class="eyebrow">Qué es</p>
    <h2>Renovación celular, por zona.</h2>
    <p class="franja__sub">Un peeling químico retira la capa superficial de la piel para que salga la de abajo, más pareja y más luminosa. Se trabaja por zonas, igual que el láser, y la profundidad se decide según tu piel.</p>
    <div class="pasos">
      <div class="paso rev"><span class="paso__n">01</span><div><h3>Para qué sirve</h3><p>Manchas, textura irregular, poros abiertos, marcas de acné y zonas oscurecidas por depilación o roce.</p></div></div>
      <div class="paso rev"><span class="paso__n">02</span><div><h3>Cuántas sesiones</h3><p>Depende de la zona y de lo que queramos corregir. Te damos el número en la valoración, no antes.</p></div></div>
      <div class="paso rev"><span class="paso__n">03</span><div><h3>Después de la sesión</h3><p>La piel puede descamarse los días siguientes. Es parte del proceso, y te explicamos cómo cuidarla.</p></div></div>
      <div class="paso rev"><span class="paso__n">04</span><div><h3>Protector solar obligatorio</h3><p>Sin él, el peeling puede dejar más mancha de la que quitó. No es una recomendación, es una condición.</p></div></div>
    </div>
  </div>
</section>
''' + conf_html("peeling",
        "Elige las zonas que quieres tratar.",
        "Toca en el cuerpo o en la lista. El mensaje llega a WhatsApp con tu selección ya escrita.",
        "Consultar mi peeling") + '''
<section class="franja franja--papel">
  <div class="env">
''' + aviso_precio("PEE","Cada zona tiene su precio y depende del tipo de peeling que necesites. Te lo decimos por WhatsApp o en la valoración.") + '''  </div>
</section>
'''
    return pagina("peeling","Peeling","Peeling químico",
        "La piel de abajo, que siempre estuvo ahí.",
        "Renovación celular por zonas: rostro, axilas, espalda, zona íntima y perianal. La profundidad se decide según tu piel.",
        cuerpo, "Peeling químico en Caracas por zonas. Centro estético en Macaracuay.",
        conf=True)


def pagina_rejuvenecimiento():
    cuerpo = f'''
{foto_ancha("pared-verde","Espacio de tratamientos de rejuvenecimiento","Nuestro espacio para inyectables")}

<section class="franja franja--menta">
  <div class="env">
    <p class="eyebrow">Los tratamientos</p>
    <h2>Cada uno resuelve algo distinto.</h2>
    <p class="franja__sub">No es lo mismo relajar una arruesta de expresión que reponer volumen o estimular colágeno. En la valoración definimos qué necesitas, y a veces la respuesta es nada.</p>
''' + servicios_html(TEN["servicios"]["rejuvenecimiento"]) + aviso_precio("REJ") + '''  </div>
</section>

<section class="franja">
  <div class="env">
    <p class="eyebrow">Antes de aplicar</p>
    <h2>Siempre hay valoración.</h2>
    <div class="pasos">
      <div class="paso rev"><span class="paso__n">01</span><div><h3>Valoración previa</h3><p>Ningún inyectable se aplica sin evaluar antes. Miramos tu rostro, escuchamos qué te molesta y te decimos qué se puede hacer y qué no.</p></div></div>
      <div class="paso rev"><span class="paso__n">02</span><div><h3>Jornadas fijas</h3><p>Bótox y rellenos se aplican miércoles y viernes. Plasma rico en plaquetas, lunes y miércoles. Se agenda aparte del resto.</p></div></div>
      <div class="paso rev"><span class="paso__n">03</span><div><h3>El bótox lleva retoque incluido</h3><p>A los quince días revisamos el resultado y ajustamos si hace falta, sin costo adicional. Está incluido en el tratamiento.</p></div></div>
      <div class="paso rev"><span class="paso__n">04</span><div><h3>El ácido hialurónico se cotiza por mililitro</h3><p>La cantidad depende de la zona y de tu caso. Labios necesitan menos que pómulos o mandíbula, y eso se define contigo antes de empezar.</p></div></div>
    </div>
  </div>
</section>
'''
    return pagina("rejuvenecimiento","Rejuvenecimiento","Rejuvenecimiento",
        "Que se note que estás mejor, no que te hiciste algo.",
        "Bótox, ácido hialurónico, PDRN y plasma rico en plaquetas. Siempre con valoración previa, y con el retoque incluido cuando corresponde.",
        cuerpo, "Bótox, ácido hialurónico y PDRN en Caracas. Centro estético en Macaracuay.")


# ═══════════════════════════════════════════════════════════════════════════
#  POLÍTICA DE PRIVACIDAD — exigida por Meta en el perfil de WhatsApp
# ═══════════════════════════════════════════════════════════════════════════
def pagina_privacidad():
    b = "../"
    cuerpo = '''
<section class="franja" style="padding-top:clamp(24px,4vw,44px)">
  <div class="env" style="max-width:760px">
    <p class="eyebrow">Documento legal</p>
    <h2 style="font-size:clamp(2rem,5vw,3.2rem);max-width:18ch">Política de privacidad</h2>
    <p class="franja__sub">Última actualización: agosto de 2026.</p>

    <div class="legal-doc">
      <h3>Quiénes somos</h3>
      <p>NADINASSPA, C.A, RIF J-50699892-0, con domicilio en Av. Macaracuay, C.C. Multicentro
      Macaracuay, Nivel 5, Oficina 5, Urb. Macaracuay, Caracas, Miranda 1071, Venezuela.
      Operamos bajo el nombre comercial Nadina&#39;s Spa.</p>
      <p>Para cualquier asunto relacionado con esta política puedes escribirnos a
      <strong>contacto@nadinasspa.com</strong> o por WhatsApp al +58 412 939 5252.</p>

      <h3>Qué datos recogemos</h3>
      <p><strong>Cuando nos escribes por WhatsApp:</strong> tu número de teléfono, tu nombre de
      perfil y el contenido de los mensajes que nos envías. Estos datos los recibimos a través
      de la plataforma de WhatsApp Business, propiedad de Meta.</p>
      <p><strong>Cuando vienes al centro:</strong> tu nombre, cédula, teléfono, y la información
      clínica y estética que sea necesaria para atenderte con seguridad: antecedentes,
      alergias, medicación relevante, tratamientos realizados y sus resultados.</p>
      <p><strong>Fotografías:</strong> solo tomamos y conservamos fotografías de tratamientos
      cuando tú lo autorizas por escrito. Las fotografías que publicamos en la web o en redes
      sociales requieren una autorización adicional y expresa, independiente de la anterior.</p>
      <p><strong>En esta página web:</strong> no usamos cookies de seguimiento, no tenemos
      publicidad, y no compartimos información con terceros con fines comerciales. Esta web es
      un sitio estático: no recoge datos de navegación ni crea perfiles de visitantes.</p>

      <h3>Para qué los usamos</h3>
      <ul>
        <li>Responder a tus consultas y agendar tus citas.</li>
        <li>Llevar tu historial de tratamientos, para que quien te atienda sepa qué se te hizo antes.</li>
        <li>Aplicar los tratamientos con seguridad, evitando lo que esté contraindicado en tu caso.</li>
        <li>Enviarte recordatorios de tus citas y seguimiento de tratamientos en curso,
        únicamente si has aceptado recibirlos.</li>
        <li>Cumplir con nuestras obligaciones fiscales y contables.</li>
      </ul>
      <p>No vendemos, alquilamos ni cedemos tus datos a terceros con fines publicitarios.</p>

      <h3>Mensajes por WhatsApp</h3>
      <p>Te escribimos por WhatsApp cuando tú has iniciado la conversación, o cuando has
      autorizado que te enviemos recordatorios. Puedes pedirnos que dejemos de escribirte en
      cualquier momento, respondiendo al mismo chat. La baja es inmediata y definitiva hasta
      que tú misma nos pidas lo contrario.</p>
      <p>WhatsApp es un servicio de Meta Platforms. El tratamiento que Meta hace de tus datos
      se rige por sus propias políticas, que no controlamos.</p>

      <h3>Cuánto tiempo los conservamos</h3>
      <p>La información clínica y de tratamientos se conserva mientras seas cliente y durante
      el tiempo que exija la normativa aplicable. Las conversaciones de WhatsApp se conservan
      el tiempo necesario para dar seguimiento a tu atención. Si nos pides que eliminemos tus
      datos, lo hacemos salvo aquello que estemos obligados a conservar por ley.</p>

      <h3>Con quién los compartimos</h3>
      <p>Con los proveedores tecnológicos que hacen funcionar nuestro sistema de gestión y
      nuestro canal de mensajería, que los tratan únicamente por cuenta nuestra y bajo
      instrucciones nuestras. Con nuestros asesores contables, para el cumplimiento de
      obligaciones fiscales. Y con las autoridades, cuando la ley lo requiera.</p>

      <h3>Cómo los protegemos</h3>
      <p>El acceso a tu información está restringido al personal que necesita consultarla para
      atenderte. Los sistemas que la almacenan cuentan con control de acceso y cifrado en
      tránsito. Ninguna medida es infalible, pero tratamos tu información clínica con el
      cuidado que corresponde a un dato de salud.</p>

      <h3>Tus derechos</h3>
      <p>Puedes pedirnos en cualquier momento que te digamos qué datos tuyos tenemos, que los
      corrijamos si están equivocados, que los eliminemos, o que dejemos de usarlos para
      enviarte mensajes. Escríbenos a <strong>contacto@nadinasspa.com</strong> o por WhatsApp
      al +58 412 939 5252, y lo resolvemos.</p>
      <p>También puedes retirar en cualquier momento la autorización que hayas dado para
      publicar tus fotografías. Si lo haces, las retiramos de la web y de nuestras redes.</p>

      <h3>Menores de edad</h3>
      <p>No atendemos a menores de edad sin la presencia y autorización de su representante
      legal, ni recogemos sus datos por otra vía.</p>

      <h3>Cambios en esta política</h3>
      <p>Si cambiamos algo relevante, actualizamos la fecha del encabezado y publicamos la
      nueva versión en esta misma dirección.</p>
    </div>
  </div>
</section>
'''
    return (cabeza("Política de privacidad · Nadina\'s Spa",
                   "Cómo trata NADINASSPA, C.A los datos personales de sus clientes.", b)
    + nav(b) + '\n<main>\n<div class="env migas"><a href="' + b + 'index.html">Inicio</a> · Política de privacidad</div>\n'
    + cuerpo + '</main>\n' + contacto(b) + "\n</body>\n</html>\n")


# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f'index.html                    {escribir("index.html", portada())//1024:3} KB')
    for slug, fn in [("laser",pagina_laser),("faciales",pagina_faciales),
                     ("corporales",pagina_corporales),("day-spa",pagina_dayspa),
                     ("peeling",pagina_peeling),("rejuvenecimiento",pagina_rejuvenecimiento),
                     ("privacidad",pagina_privacidad)]:
        n = escribir(f"{slug}/index.html", fn())
        print(f'{slug}/index.html{" "*(20-len(slug))}{n//1024:3} KB')
