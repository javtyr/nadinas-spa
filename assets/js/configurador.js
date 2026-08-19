/* ===========================================================================
   CONFIGURADOR DE ZONAS
   Se usa en la página de láser y en la de peeling. La diferencia es solo
   el conjunto de zonas, que se indica con data-set en el contenedor.
   Sin precios: su trabajo es armar el contexto que viaja a WhatsApp.
   =========================================================================== */
(function(){
"use strict";
const raiz = document.getElementById("conf");
if (!raiz || !window.TENANT) return;
const T = window.TENANT;
const SET = raiz.dataset.set;              // "laser" | "peeling"
const DATOS = T[SET];
if (!DATOS) return;

const FORMAS = {
  frente:{
    bozo:[[113,48,34,11]], menton:[[109,48,42,26]], barba:[[105,46,50,32]],
    orejas:[[103,30,10,18],[147,30,10,18]], hombros:[[82,98,96,22]],
    axilas:[[90,124,22,32],[148,124,22,32]], brazos:[[62,140,30,130],[168,140,30,130]],
    pecho:[[100,124,60,62]], abdomen:[[100,190,60,74]], "pecho-abd":[[100,124,60,140]],
    bikini:[[108,294,44,30]], brasilero:[[102,286,56,46]],
    "media-pierna":[[80,462,100,120]], pierna:[[80,344,100,238]]
  },
  espalda:{
    espalda:[[94,110,72,150]], "espalda-baja":[[96,206,68,64]], gluteos:[[90,286,80,60]],
    brazos:[[62,140,30,130],[168,140,30,130]],
    "media-pierna":[[80,462,100,120]], pierna:[[80,344,100,238]]
  }
};

const st = { genero:"damas", vista:"frente", sel:new Set() };
const $  = function(s){ return raiz.querySelector(s); };
const $$ = function(s){ return [].slice.call(raiz.querySelectorAll(s)); };
const lista = function(){ return DATOS[st.genero]; };
const porId = function(id){ return lista().find(function(s){ return s.id === id; }); };

function pintarCuerpo(){
  $("#figura").setAttribute("clip-path", st.genero === "damas" ? "url(#cp-d)" : "url(#cp-c)");
  const area = function(z){ return (FORMAS[st.vista][z]||[]).reduce(function(a,f){ return a+f[2]*f[3]; },0); };
  const zonas = Object.keys(lista().filter(function(s){ return s.vista === st.vista; })
      .reduce(function(o,s){ o[s.zona]=1; return o; }, {}))
      .sort(function(a,b){ return area(b)-area(a); });
  const g = $("#zonas"); g.innerHTML = "";
  zonas.forEach(function(z){
    (FORMAS[st.vista][z]||[]).forEach(function(f){
      const r = document.createElementNS("http://www.w3.org/2000/svg","rect");
      r.setAttribute("x",f[0]); r.setAttribute("y",f[1]);
      r.setAttribute("width",f[2]); r.setAttribute("height",f[3]);
      r.setAttribute("rx", Math.min(f[2],f[3])/2.6);
      r.setAttribute("class","zona"); r.dataset.zona = z;
      r.setAttribute("tabindex","0"); r.setAttribute("role","button");
      const s = lista().find(function(x){ return x.zona===z && x.vista===st.vista; });
      if (s) r.setAttribute("aria-label", s.nombre);
      g.appendChild(r);
    });
  });
  marcar();
}
function marcar(){
  const act = {};
  st.sel.forEach(function(id){ const s = porId(id); if (s) act[s.zona] = 1; });
  $$(".zona").forEach(function(r){ r.classList.toggle("on", !!act[r.dataset.zona]); });
}
function pintarChips(){
  $("#chips").innerHTML = lista().map(function(s){
    return '<button class="chip" data-id="'+s.id+'" aria-pressed="'+st.sel.has(s.id)+'">'+s.nombre+'</button>';
  }).join("");
}
function pintarCesta(){
  const ids = [].slice.call(st.sel), hay = ids.length > 0;
  $("#vacia").hidden = hay; $("#acciones").hidden = !hay;
  $("#items").innerHTML = ids.map(function(id){
    const s = porId(id); if (!s) return "";
    return '<li><span>'+s.nombre+'</span><button class="quitar" data-q="'+id+'" aria-label="Quitar '+s.nombre+'">\u00D7</button></li>';
  }).join("");
  $$(".chip").forEach(function(c){ c.setAttribute("aria-pressed", st.sel.has(c.dataset.id)); });
  marcar(); guardarURL(); enlace();
}
function enlace(){
  const ids = [].slice.call(st.sel); if (!ids.length) return;
  const nombres = ids.map(function(id){ return "\u2022 " + porId(id).nombre; }).join("\n");
  const qué = SET === "laser" ? "depilación láser" : "peeling";
  const msg = "Hola, vi la página y me interesa " + qué + ".\n\nMe gustaría:\n" + nombres +
              "\n\n\u00BFMe dan precios y disponibilidad?";
  const tok = SET === "laser" ? "LSR" : "PEE";
  $$(".js-cotiza").forEach(function(a){
    a.href = window.waURL(msg, tok, ids.join(","));
    a.target = "_blank"; a.rel = "noopener";
  });
}
function guardarURL(){
  const p = new URLSearchParams(); p.set("g", st.genero);
  if (st.sel.size) p.set("z", [].slice.call(st.sel).join(","));
  history.replaceState(null, "", st.sel.size ? "#"+p : location.pathname);
}
function leerURL(){
  if (!location.hash) return;
  const p = new URLSearchParams(location.hash.slice(1));
  if (p.get("g") === "caballeros") st.genero = "caballeros";
  (p.get("z")||"").split(",").filter(Boolean).forEach(function(id){ st.sel.add(id); });
  $$("[data-g]").forEach(function(b){ b.setAttribute("aria-pressed", b.dataset.g === st.genero); });
}
function sinc(attr,val){ $$("[data-"+attr+"]").forEach(function(b){ b.setAttribute("aria-pressed", b.dataset[attr]===val); }); }

raiz.addEventListener("click", function(e){
  const z = e.target.closest(".zona");
  if (z){
    const s = lista().find(function(x){ return x.zona===z.dataset.zona && x.vista===st.vista; });
    if (s){ st.sel.has(s.id) ? st.sel.delete(s.id) : st.sel.add(s.id); pintarCesta(); }
    return;
  }
  const chip = e.target.closest(".chip");
  if (chip){
    const s = porId(chip.dataset.id);
    if (s && s.vista !== st.vista){ st.vista = s.vista; sinc("v", st.vista); pintarCuerpo(); }
    st.sel.has(chip.dataset.id) ? st.sel.delete(chip.dataset.id) : st.sel.add(chip.dataset.id);
    pintarCesta(); return;
  }
  const q = e.target.closest("[data-q]");
  if (q){ st.sel.delete(q.dataset.q); pintarCesta(); return; }
  const bg = e.target.closest("[data-g]");
  if (bg){ st.genero = bg.dataset.g; st.sel.clear(); sinc("g",st.genero); pintarCuerpo(); pintarChips(); pintarCesta(); return; }
  const bv = e.target.closest("[data-v]");
  if (bv){ st.vista = bv.dataset.v; sinc("v",st.vista); pintarCuerpo(); return; }
});
raiz.addEventListener("keydown", function(e){
  if ((e.key==="Enter"||e.key===" ") && e.target.classList && e.target.classList.contains("zona")){
    e.preventDefault(); e.target.dispatchEvent(new MouseEvent("click",{bubbles:true}));
  }
});
const PISTA = $("#pista");
["mouseover","focusin"].forEach(function(ev){ raiz.addEventListener(ev, function(e){
  const z = e.target.closest ? e.target.closest(".zona") : null; if (!z) return;
  const s = lista().find(function(x){ return x.zona===z.dataset.zona && x.vista===st.vista; });
  if (s) PISTA.textContent = s.nombre;
}); });
["mouseout","focusout"].forEach(function(ev){ raiz.addEventListener(ev, function(e){
  if (e.target.closest && e.target.closest(".zona")) PISTA.textContent = "Toca una zona";
}); });

leerURL(); pintarCuerpo(); pintarChips(); pintarCesta();
})();
