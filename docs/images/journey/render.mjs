import { render } from "pele";
import fs from "node:fs";
const [inp, out, css, defs] = process.argv.slice(2);
const r = render(fs.readFileSync(inp, "utf8"), { limit: 1_000_000, outputLimit: 8_000_000, maxEdges: 10_000, fontSize: 16 });
const svg = r.svg.replace(/(<svg[^>]*>)/, `$1<style>${fs.readFileSync(css,"utf8")}</style>${fs.readFileSync(defs,"utf8")}`);
fs.writeFileSync(out, svg);
console.log(r.width, r.height);
