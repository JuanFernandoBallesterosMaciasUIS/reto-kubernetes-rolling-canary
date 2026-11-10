// Simulador de tráfico: lanza N peticiones al Service y resume qué versión respondió y cuántos errores hubo.
// Uso: node scripts/traffic.js [url] [peticiones] [intervalo_ms]
const http = require('http');
const url = process.argv[2] || 'http://localhost:30080/';
const total = parseInt(process.argv[3] || '100', 10);
const delay = parseInt(process.argv[4] || '50', 10);
const stats = {}; let ok = 0, fail = 0, netErr = 0;

function hit() {
  return new Promise((resolve) => {
    const req = http.get(url, { agent: false, timeout: 2000 }, (res) => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        let v = '?'; try { v = JSON.parse(d).version; } catch {}
        const key = `${v} -> HTTP ${res.statusCode}`;
        stats[key] = (stats[key] || 0) + 1;
        res.statusCode < 500 ? ok++ : fail++;
        resolve();
      });
    });
    req.on('error', () => { netErr++; resolve(); });
    req.on('timeout', () => req.destroy());
  });
}

(async () => {
  const t0 = Date.now();
  for (let i = 0; i < total; i++) { await hit(); if (delay) await new Promise(r => setTimeout(r, delay)); }
  console.log(`Simulación de tráfico: ${total} peticiones a ${url} en ${((Date.now()-t0)/1000).toFixed(1)}s`);
  console.log('-----------------------------------------------');
  for (const [k, n] of Object.entries(stats).sort()) {
    console.log(`${k.padEnd(20)} ${String(n).padStart(4)}  (${(100*n/total).toFixed(1)}%)  ${'#'.repeat(Math.round(40*n/total))}`);
  }
  console.log('-----------------------------------------------');
  console.log(`Exitosas: ${ok}   Errores 5xx: ${fail}   Errores de red: ${netErr}   Disponibilidad: ${(100*ok/total).toFixed(1)}%`);
})();
