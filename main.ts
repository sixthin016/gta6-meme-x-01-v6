// gta6-meme-x-01-v6 — main.ts
// Copies POST.json from the repo into /output. Nothing else.
// Node 22 stdlib only, deterministic, no network, no clock.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "POST.json"), join(outDir, "POST.json"));
console.log("copied POST.json to /output/POST.json");
