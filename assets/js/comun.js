/* ===========================================================================
   COMÚN — se carga en todas las páginas
   =========================================================================== */
(function(){
"use strict";
if (!window.TENANT) return;
const T = window.TENANT, C = T.config;

/* ---- resolución de medios ----
   Todo lo que sea foto o video pasa por aquí. Si config.medios_base está vacío,
   se sirven del repositorio; si tiene una URL, se sirven de ahí. -------------- */
window.medio = function(nombre, ext){
  const base = C.medios_base || ((document.body.dataset.base||"") + "assets/img/");
  return base + nombre + (ext || ".webp");
};

/* al cargar, reescribe cualquier <img data-medio="nombre"> */
document.querySelectorAll("[data-medio]").forEach(function(el){
  el.src = window.medio(el.dataset.medio, el.dataset.ext);
});

/* ---- enlaces de WhatsApp con token de origen ----
   Formato: [NS·SECCION·detalle]
   El agente de Javtyr lo detecta en el primer mensaje y entra por el flujo
   de cotización con el contexto ya resuelto. -------------------------------- */
window.waURL = function(msg, tok, detalle){
  const sello = "[NS\u00B7" + tok + (detalle ? "\u00B7" + detalle : "") + "]";
  return "https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(msg + "\n\n" + sello);
};

document.querySelectorAll(".js-wa").forEach(function(a){
  a.href = window.waURL(a.dataset.msg || "Hola, quiero información.", a.dataset.tok || "GEN");
  a.target = "_blank"; a.rel = "noopener";
});

/* ---- foto de portada ---- */
(function portada(){
  const c = document.querySelector(".marco"); if (!c) return;
  const p = (window.MEDIOS || {}).portada || {};
  if (p.video){
    c.innerHTML = '<video src="' + window.medio(p.video, ".mp4") + '"' +
      (p.poster ? ' poster="' + window.medio(p.poster) + '"' : '') +
      ' autoplay muted loop playsinline preload="metadata"></video>';
    c.style.padding = "0";
  } else if (p.foto){
    c.innerHTML = '<img src="' + window.medio(p.foto) + '" alt="' + (p.alt||"") + '">';
    c.style.padding = "0";
  }
})();

/* ---- revelado al hacer scroll ---- */
const io = new IntersectionObserver(function(es){
  es.forEach(function(x){ if (x.isIntersecting){ x.target.classList.add("ver"); io.unobserve(x.target); } });
}, {threshold:.14});
document.querySelectorAll(".rev").forEach(function(el){ io.observe(el); });

(function retrato(){
  const c = document.getElementById("foto-fundadora"); if (!c) return;
  const f = (window.MEDIOS || {}).fundadora || {};
  if (f.foto) c.innerHTML = '<img src="' + window.medio(f.foto) + '" alt="' + (f.alt||"") + '" loading="lazy">';
})();

const anio = document.getElementById("anio");
if (anio) anio.textContent = new Date().getFullYear();
})();
