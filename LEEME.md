# Nadina's Spa — sitio web

Sitio estático de siete páginas. Sin backend, sin base de datos, sin costo de hosting.

## Publicar (15 minutos)

1. Repositorio **público** llamado `nadinas-spa`.
2. Subir todo el contenido de esta carpeta a la raíz.
3. **Settings → Pages → Source: `main` / `root`.**
4. En dos minutos está en `https://TUUSUARIO.github.io/nadinas-spa`.

## Estructura

```
index.html                 portada: hero, las seis puertas, tecnología, Gift Cards
laser/                     configurador de zonas + Soprano Titanium + formas de pago
faciales/                  los once pasos de la limpieza profunda
corporales/                masajes y packs reductores
day-spa/                   las cuatro opciones + Gift Cards
peeling/                   configurador de zonas de peeling
rejuvenecimiento/          inyectables, con valoración previa
```

## Dónde se edita cada cosa

| Qué cambiar | Archivo |
|---|---|
| Servicios, categorías, zonas, WhatsApp, horario | `assets/js/datos.js` |
| **Mostrar u ocultar precios** | `datos.js` → `config.mostrar_precios` |
| Fotos y video | `assets/js/datos.js` → `window.MEDIOS` |
| Estilos | `assets/css/estilo.css` |
| Textos de cada página | el `index.html` de cada carpeta |

Para regenerar las páginas tras editar textos en `gen.py`: `python3 gen.py`

## Los precios están apagados

`config.mostrar_precios` está en `false`. Toda la página lleva a WhatsApp a consultar.
La lógica de precios sigue escrita: el día que se decida mostrarlos, se cambia ese campo.

## Las fotos

Las actuales son provisionales, recortadas de las que envió el spa. Se sustituyen por
las de la sesión sin tocar el HTML: mismo nombre de archivo en `assets/img/`.

Formato: WebP, máximo 1600 px de ancho. El script `optimizar-fotos.sh` hace la conversión.

## El token de origen

Cada botón manda a WhatsApp con un token al final del mensaje:

```
[NS·LSR·d-axilas,d-brasilero,d-media-p]
```

Códigos: `LSR` láser · `PEE` peeling · `FAC` faciales · `COR` corporales · `DAY` day spa ·
`REJ` rejuvenecimiento · `GIFT` gift cards · `NAV`, `HERO`, `PIE`, `TEL`, `FLOT` botones generales.

El agente de Javtyr debe detectarlo y entrar por el flujo de cotización, **no por el
clasificador general**. Los identificadores de zona son provisionales: hay que
sustituirlos por los `service_id` reales del catálogo.

## Dominio propio

1. Comprar `nadinasspa.com` (Cloudflare Registrar, ~$10/año).
2. `CNAME` de `www` hacia `TUUSUARIO.github.io` + los cuatro registros `A` de GitHub Pages.
3. **Settings → Pages → Custom domain**, marcar **Enforce HTTPS**.

---

## Dónde viven las fotos y los videos

Todo pasa por un solo campo en `assets/js/datos.js`:

```js
config: {
  medios_base: ""        // ← del propio repositorio
}
```

| Valor | De dónde se sirven |
|---|---|
| `""` | Del repositorio, carpeta `assets/img/`. Es lo actual |
| `"https://cdn.javtyr.com/nadinas/"` | De S3 vía CloudFront |
| `"https://res.cloudinary.com/.../"` | De Cloudinary |

Cambiar esa línea mueve **todos** los medios de sitio. No hay ninguna ruta de imagen
escrita a mano en el HTML: las `<img>` usan `data-medio="nombre"` y el JavaScript
resuelve la URL completa.

Para migrar a S3:

1. Subir el contenido de `assets/img/` a `s3://javtyr-medios/tenants/nadinas/publico/`
2. Poner CloudFront delante, con el bucket privado y acceso solo desde la distribución
3. Cambiar `medios_base` por la URL de CloudFront con barra final
4. Borrar `assets/img/` del repositorio (queda en el historial de git por si acaso)

### Regla de datos sensibles

Las fotos de antes y después son datos de salud. Las que se publican van al bucket
público **solo con consentimiento firmado**. El archivo clínico de seguimiento de cada
paciente **nunca** va a un repositorio público ni a un bucket de lectura abierta.

### Video

Convertir siempre antes de subir, en la máquina local, nunca en el servidor de producción:

```bash
ffmpeg -i original.MOV -vf "scale=-2:1280" -c:v libx264 -crf 26 \
       -preset slow -profile:v high -pix_fmt yuv420p -an \
       -movflags +faststart hero.mp4
```

Los iPhone graban en HEVC y ese códec no reproduce fuera de Safari. Un clip de 8 segundos
convertido a H.264 queda en 1,5 a 3 MB, así que no hace falta ningún servicio de streaming.
