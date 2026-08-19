/* ===========================================================================
   DATOS DEL TENANT — Nadina's Spa
   ---------------------------------------------------------------------------
   Esta estructura imita la respuesta del futuro endpoint de Javtyr:
       GET /api/public/{tenant}/pagina
   Cuando exista, se reemplaza este archivo por un fetch y nada más cambia.

   `config` es la parte que varía de un tenant a otro. Es lo que después
   vivirá como campos configurables al dar de alta un negocio nuevo.
   =========================================================================== */

window.TENANT = {
  slug: "nadinas",
  nombre: "Nadina's Spa",
  nombre_legal: "Nadinas SPA",
  actualizado: "2026-08-19",

  /* ---- configuración de presentación (por tenant) ---- */
  config: {
    mostrar_precios: false,      // ← ponlo en true y aparecen los precios
    monedas: ["usd","bs"],       // con una sola, el interruptor no se dibuja
    factor_eur: 1.40,            // solo se usa si mostrar_precios es true
    contacto: ["whatsapp"],      // whatsapp | webchat | instagram | telefono
    whatsapp: "584142863713",
    instagram: "nadinasspa",
    direccion: ["C.C. Multicentro Macaracuay","Urbanización Macaracuay, Caracas"],
    nota_direccion: "Te enviamos la ubicación exacta al confirmar tu cita.",
    horario: ["Lunes a viernes · 9:00 – 18:00","Sábados · 10:00 – 14:00","Domingos cerrado"],
    equipo_estrella: "Alma Soprano Titanium",

    /* ---- de dónde salen las fotos y los videos ----
       ""                                    → del propio repositorio (assets/img/)
       "https://cdn.javtyr.com/nadinas/"     → de S3 vía CloudFront
       "https://res.cloudinary.com/xx/..."   → de Cloudinary
       Cambiar esta línea mueve TODOS los medios de sitio. Nada más se toca.
       Tiene que terminar en barra. */
    medios_base: ""
  },

  /* ---- las seis puertas, en el mismo orden que el menú del agente ---- */
  categorias: [
    { slug:"laser", nombre:"Depilación láser", destacada:true,
      resumen:"Alma Soprano Titanium, tres longitudes de onda a la vez. 26 zonas para damas y caballeros, con valoración antes de empezar.",
      corto:"Soprano Titanium · 26 zonas", img:"cat-laser" },
    { slug:"faciales", nombre:"Faciales",
      resumen:"Limpiezas profundas, exosomas y nutrición para tu rostro.",
      corto:"Limpiezas, exosomas, nutrición", img:"cat-faciales" },
    { slug:"corporales", nombre:"Corporales",
      resumen:"Masajes relajantes, reductores y tratamientos para moldear.",
      corto:"Masajes y reductores", img:"cat-corporales" },
    { slug:"day-spa", nombre:"Nadina's Day Spa",
      resumen:"Paquetes para cumpleaños, aniversarios y días de relax.",
      corto:"Cumpleaños y aniversarios", img:"cat-dayspa" },
    { slug:"peeling", nombre:"Peeling",
      resumen:"Renovación celular para una piel luminosa y sin manchas.",
      corto:"Renovación por zona", img:"cat-peeling" },
    { slug:"rejuvenecimiento", nombre:"Rejuvenecimiento",
      resumen:"Bótox, ácido hialurónico, PDRN y plasma, con valoración previa.",
      corto:"Bótox, ácido hialurónico, PDRN", img:"cat-rejuvenecimiento" }
  ],

  /* ---- zonas de láser para el configurador ---- */
  laser: {
    damas: [
      { id:"d-bozo",      nombre:"Bozo",                    zona:"bozo",        vista:"frente" },
      { id:"d-bozo-ment", nombre:"Bozo y mentón",           zona:"menton",      vista:"frente" },
      { id:"d-axilas",    nombre:"Axilas",                  zona:"axilas",      vista:"frente" },
      { id:"d-brazos",    nombre:"Brazos",                  zona:"brazos",      vista:"frente" },
      { id:"d-pecho",     nombre:"Pecho",                   zona:"pecho",       vista:"frente" },
      { id:"d-abdomen",   nombre:"Abdomen",                 zona:"abdomen",     vista:"frente" },
      { id:"d-pecho-abd", nombre:"Pecho y abdomen",         zona:"pecho-abd",   vista:"frente" },
      { id:"d-bikini",    nombre:"Bikini",                  zona:"bikini",      vista:"frente" },
      { id:"d-brasilero", nombre:"Brasilero (full bikini)", zona:"brasilero",   vista:"frente" },
      { id:"d-media-p",   nombre:"Media pierna",            zona:"media-pierna",vista:"frente" },
      { id:"d-pierna",    nombre:"Pierna completa",         zona:"pierna",      vista:"frente" },
      { id:"d-espalda",   nombre:"Espalda",                 zona:"espalda",     vista:"espalda" },
      { id:"d-gluteos",   nombre:"Glúteos",                 zona:"gluteos",     vista:"espalda" }
    ],
    caballeros: [
      { id:"c-barba",    nombre:"Barba",            zona:"barba",       vista:"frente" },
      { id:"c-orejas",   nombre:"Orejas",           zona:"orejas",      vista:"frente" },
      { id:"c-axilas",   nombre:"Axilas",           zona:"axilas",      vista:"frente" },
      { id:"c-hombros",  nombre:"Hombros",          zona:"hombros",     vista:"frente" },
      { id:"c-brazos",   nombre:"Brazos",           zona:"brazos",      vista:"frente" },
      { id:"c-pecho",    nombre:"Pecho",            zona:"pecho",       vista:"frente" },
      { id:"c-abdomen",  nombre:"Abdomen",          zona:"abdomen",     vista:"frente" },
      { id:"c-intima",   nombre:"Zona íntima",      zona:"brasilero",   vista:"frente" },
      { id:"c-media-p",  nombre:"Media pierna",     zona:"media-pierna",vista:"frente" },
      { id:"c-pierna",   nombre:"Pierna completa",  zona:"pierna",      vista:"frente" },
      { id:"c-espalda",  nombre:"Espalda completa", zona:"espalda",     vista:"espalda" },
      { id:"c-esp-baja", nombre:"Espalda baja",     zona:"espalda-baja",vista:"espalda" },
      { id:"c-gluteos",  nombre:"Glúteos",          zona:"gluteos",     vista:"espalda" }
    ]
  },

  /* ---- zonas de peeling: reutilizan el mismo configurador ---- */
  peeling: {
    damas: [
      { id:"p-rostro",   nombre:"Rostro",       zona:"menton",    vista:"frente" },
      { id:"p-axilas",   nombre:"Axilas",       zona:"axilas",    vista:"frente" },
      { id:"p-intima",   nombre:"Zona íntima",  zona:"brasilero", vista:"frente" },
      { id:"p-espalda",  nombre:"Espalda",      zona:"espalda",   vista:"espalda" },
      { id:"p-perianal", nombre:"Zona perianal",zona:"gluteos",   vista:"espalda" }
    ],
    caballeros: [
      { id:"p-rostro-c",   nombre:"Rostro",       zona:"barba",     vista:"frente" },
      { id:"p-axilas-c",   nombre:"Axilas",       zona:"axilas",    vista:"frente" },
      { id:"p-intima-c",   nombre:"Zona íntima",  zona:"brasilero", vista:"frente" },
      { id:"p-espalda-c",  nombre:"Espalda",      zona:"espalda",   vista:"espalda" },
      { id:"p-perianal-c", nombre:"Zona perianal",zona:"gluteos",   vista:"espalda" }
    ]
  },

  /* ---- servicios por categoría, sin precio ---- */
  servicios: {
    faciales: [
      { n:"Limpieza facial profunda premium", d:"Diagnóstico, higienización, exfoliación, vapor ozono, extracción, paleta ultrasónica, alta frecuencia, martillo frío, mascarilla descongestiva, hidratación con máscara led y protector solar." },
      { n:"Limpieza facial con Hidrafacial", d:"Limpieza profunda con tecnología de hidradermoabrasión." }
    ],
    corporales: [
      { n:"Pack reductor maderoterapia", d:"Cinco sesiones de maderoterapia, radiofrecuencia y drenaje linfático. Incluye papel reductor osmótico." },
      { n:"Pack reductor aparatología", d:"Cinco sesiones de lipoláser, ultracavitación, drenaje linfático y radiofrecuencia. Incluye papel reductor osmótico." },
      { n:"Masaje reductivo", d:"Por sesión suelta, para complementar el pack o por su cuenta." },
      { n:"Masaje relajante", d:"Espalda y cuello, o cuerpo completo. Presión ajustable." },
      { n:"Masaje descontracturante", d:"Trabajo profundo sobre nudos y zonas de tensión localizada." },
      { n:"Masaje de pies y gemelos", d:"Para quien pasa el día de pie o entrena." },
      { n:"Piedras calientes", d:"Espalda y cuello, o cuerpo completo. Calor sostenido para soltar tensión antigua." }
    ],
    "day-spa": [
      { n:"Estándar · una persona", d:"Limpieza facial profunda con ácido hialurónico y oro de 24 quilates, masaje relajante con aceites aromáticos, musicoterapia y aromaterapia." },
      { n:"Estándar · dos personas", d:"La misma experiencia, en cabina compartida." },
      { n:"Premium · una persona", d:"Todo lo del estándar más exfoliación de espalda, detalle sorpresa de flores o chocolate, copa de vino o espumante y decoración de cabina." },
      { n:"Premium · dos personas", d:"La versión completa, para celebrar en pareja o entre amigas." }
    ],
    rejuvenecimiento: [
      { n:"Bótox facial", d:"Frente, entrecejo y patas de gallo.", u:"Incluye retoque a los 15 días" },
      { n:"Bótox de axilas", d:"Para hiperhidrosis, la sudoración excesiva." },
      { n:"Ácido hialurónico", d:"Labios, surcos, mandíbula y pómulos. La cantidad se define en la valoración.", u:"Se cotiza por mililitro" },
      { n:"Ojeras · hundimiento", d:"Ácido hialurónico de baja reticulación para recuperar volumen." },
      { n:"Ojeras · Nucleofill eyes", d:"Estimulación de colágeno en el contorno." },
      { n:"Ojeras · pigmentación", d:"Peeling aclarante mesoestetic." },
      { n:"PDRN · polinucleótidos", d:"Regeneración celular, colágeno y elastina. Gama media y gama alta según el caso: cicatrices de acné, poros abiertos y manchas." },
      { n:"Papada", d:"Lipolíticos aplicados por mesoterapia." },
      { n:"Plasma rico en plaquetas", d:"Incluye higienización facial, aplicación con mesoterapia y mascarilla nutritiva.", u:"Jornadas lunes y miércoles" }
    ]
  }
};

/* ---------------------------------------------------------------------------
   MEDIOS — el único sitio donde se declaran fotos y videos.
   Mientras un campo sea null, la página muestra un marcador.
   --------------------------------------------------------------------------- */
window.MEDIOS = {
  portada: { video:null, poster:null, foto:"hero-recepcion", alt:"Recepción de Nadina's Spa" },
  fundadora: { foto:null, alt:"Fundadora de Nadina's Spa" },
  resultados: []   // cada entrada necesita antes y después para aparecer
};
