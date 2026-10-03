import fs from "node:fs";

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exitCode = 1;
  } else {
    console.log(`PASS: ${message}`);
  }
}

const html = fs.readFileSync("index.html", "utf8");
const publicApi = fs.readFileSync("api/control-state.js", "utf8");
const privateApi = fs.readFileSync("api/private-state.js", "utf8");
const submarine = JSON.parse(fs.readFileSync("control/submarine-config.json", "utf8"));

assert(html.includes('id="control-section"'), "live control section exists");
assert((html.match(/data-section=/g) || []).length === 12, "12 navigation destinations");
assert(html.includes("/api/control-state"), "public control API wired");
assert(html.includes("/api/private-state"), "private control API wired");
assert(html.includes('@media (max-width:1024px)'), "1024px mobile hardening preserved");
assert(html.includes('@media (max-width:600px)') || html.includes('@media(max-width:600px)'), "600px mobile hardening preserved");
assert(html.includes('@media (max-width:360px)'), "360px mobile hardening preserved");

for (const [i, script] of [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).entries()) {
  try {
    new Function(script);
    console.log(`PASS: inline script #${i + 1} parses`);
  } catch (error) {
    console.error(`FAIL: inline script #${i + 1} syntax — ${error.message}`);
    process.exitCode = 1;
  }
}

for (const [name, source] of [["public API", publicApi], ["private API", privateApi]]) {
  try {
    new Function("require", "module", "exports", source);
    console.log(`PASS: ${name} parses`);
  } catch (error) {
    console.error(`FAIL: ${name} syntax — ${error.message}`);
    process.exitCode = 1;
  }
}

assert(publicApi.includes('exposure: "PUBLIC_SANITIZED"'), "public API explicitly sanitized");
assert(publicApi.includes("privateDataExposed: false"), "public API claims no private exposure");
assert(!publicApi.includes("GOOGLE_REFRESH_TOKEN"), "public API has no Google private credential path");
assert(privateApi.includes('res.setHeader("Cache-Control", "no-store")'), "private API disables caching");
assert(privateApi.includes("timingSafeEqual"), "private token comparison is timing-safe");
assert(privateApi.includes('privateState: "LOCKED"'), "private API has explicit locked state");
assert(privateApi.includes('reason === "not_configured" ? 503 : 401'), "private API fails closed when auth is absent/invalid");

assert(submarine.mode === "OFF", "Submarine mode is OFF");
assert(submarine.writeAuthority === false, "Submarine has no write authority");
assert(submarine.wipLimit === 1, "Submarine WIP limit remains 1");
assert(submarine.humanGates.includes("merge"), "merge remains Human Gate");
assert(submarine.humanGates.includes("deploy"), "deploy remains Human Gate");
assert(submarine.humanGates.includes("production"), "production remains Human Gate");
assert(submarine.humanGates.includes("live-database"), "live DB remains Human Gate");
assert(submarine.humanGates.includes("secrets"), "secrets remain Human Gate");

if (process.exitCode) {
  console.error("\nCOMMAND_CENTER_CONTROL_VALIDATION=FAIL");
  process.exit(process.exitCode);
}

console.log("\nCOMMAND_CENTER_CONTROL_VALIDATION=PASS");
