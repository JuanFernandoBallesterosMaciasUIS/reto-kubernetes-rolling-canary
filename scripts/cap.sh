# cap <nombre> <comando...> : ejecuta el comando y guarda "$ comando" + salida en capturas/txt/<nombre>.txt
cap() { local n="$1"; shift; { echo "\$ $*"; eval "$@" 2>&1; } | sed 's/\r$//' > "capturas/txt/$n.txt"; cat "capturas/txt/$n.txt"; echo; }
