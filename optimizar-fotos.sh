#!/usr/bin/env bash
# ============================================================================
#  optimizar-fotos.sh — deja las fotos listas para la web
# ----------------------------------------------------------------------------
#  Convierte a WebP, reduce el tamaño y renombra sin acentos ni espacios.
#  Una foto de 4 MB del fotógrafo queda en ~180 KB sin diferencia visible.
#
#  USO:
#    ./optimizar-fotos.sh ~/Downloads/sesion-fotos  fundadora
#                         └ carpeta con los originales └ subcarpeta destino
#
#  Subcarpetas: hero · fundadora · espacios · equipos · tratamientos · resultados
#
#  REQUISITO: ImageMagick.
#    macOS:   brew install imagemagick
#    Ubuntu:  sudo apt install imagemagick
#    Windows: usar Git Bash con ImageMagick instalado, o WSL
# ============================================================================
set -euo pipefail

ORIGEN="${1:-}"
GRUPO="${2:-}"

if [[ -z "$ORIGEN" || -z "$GRUPO" ]]; then
  echo "Uso: ./optimizar-fotos.sh <carpeta-con-originales> <subcarpeta-destino>"
  echo "Ejemplo: ./optimizar-fotos.sh ~/Downloads/sesion fundadora"
  exit 1
fi
if [[ ! -d "$ORIGEN" ]]; then
  echo "No existe la carpeta: $ORIGEN"
  exit 1
fi
if ! command -v magick >/dev/null 2>&1 && ! command -v convert >/dev/null 2>&1; then
  echo "Falta ImageMagick. Instálalo y vuelve a intentar."
  exit 1
fi
MAGICK=$(command -v magick || command -v convert)

DESTINO="assets/img/$GRUPO"
mkdir -p "$DESTINO"

# La portada admite más resolución porque ocupa toda la pantalla.
if [[ "$GRUPO" == "hero" ]]; then ANCHO=2400; else ANCHO=1600; fi

n=0
shopt -s nullglob nocaseglob
for f in "$ORIGEN"/*.{jpg,jpeg,png,heic,tif,tiff}; do
  n=$((n+1))
  salida=$(printf "%s/%s-%02d.webp" "$DESTINO" "$GRUPO" "$n")
  "$MAGICK" "$f" \
    -auto-orient \
    -resize "${ANCHO}x${ANCHO}>" \
    -strip \
    -quality 82 \
    "$salida"
  antes=$(du -k "$f"      | cut -f1)
  luego=$(du -k "$salida" | cut -f1)
  printf "  %-42s %6s KB → %5s KB\n" "$(basename "$salida")" "$antes" "$luego"
done

if [[ $n -eq 0 ]]; then
  echo "No se encontraron imágenes en $ORIGEN"
  exit 0
fi

echo ""
echo "$n imágenes listas en $DESTINO"
echo "Ahora declara las que vayas a usar en assets/js/medios.js"
echo ""
echo "Recuerda: la primera pantalla completa no debe pasar de 1 MB."
