// App de demostración para el Reto 3 - Estrategias de despliegue en Kubernetes
// La versión y el "modo de fallo" se fijan en la imagen (build-arg), así cada tag = una versión.
const http = require('http');
const os = require('os');

const VERSION   = process.env.APP_VERSION || 'v0';
const COLOR     = process.env.APP_COLOR   || 'gray';
const FAIL_MODE = process.env.FAIL_MODE   || 'none'; // none | crash | errors
const PORT      = 8080;
const started   = Date.now();

if (FAIL_MODE === 'crash') {
  // Escenario de fallo 1: la nueva versión no arranca (p.ej. variable de config faltante)
  console.error(`[${VERSION}] ERROR FATAL: falta variable DATABASE_URL. Abortando.`);
  setTimeout(() => process.exit(1), 1500);
}

const server = http.createServer((req, res) => {
  if (req.url === '/healthz') {               // usado por readiness/liveness
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    return res.end('ok');
  }
  if (FAIL_MODE === 'errors') {               // Escenario de fallo 2: arranca y pasa probes, pero falla con usuarios reales
    res.writeHead(500, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ version: VERSION, pod: os.hostname(), error: 'NullPointer en /checkout' }));
  }
  const body = { version: VERSION, color: COLOR, pod: os.hostname(), uptime_s: Math.round((Date.now() - started) / 1000) };
  if ((req.headers.accept || '').includes('text/html')) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(`<!doctype html><html><head><title>Reto 3 - ${VERSION}</title></head>
<body style="font-family:Segoe UI,Arial;background:${COLOR};color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
<div style="text-align:center"><h1 style="font-size:64px;margin:0">Tienda UIS &mdash; ${VERSION}</h1>
<p style="font-size:24px">Atendido por el pod <b>${os.hostname()}</b></p></div></body></html>`);
  }
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
});

server.listen(PORT, () => console.log(`[${VERSION}] escuchando en :${PORT} (FAIL_MODE=${FAIL_MODE})`));
process.on('SIGTERM', () => { console.log(`[${VERSION}] SIGTERM recibido, cerrando...`); server.close(() => process.exit(0)); });
