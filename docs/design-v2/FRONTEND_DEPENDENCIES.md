# REGISTRO DELLE DIPENDENZE FRONTEND — design V2

Stato: **APERTO** · Regola: nessuna dipendenza entra senza una riga qui, e nessuna riga qui
descrive una dipendenza che non è stata misurata.

---

## 0. Perché questo registro esiste

Fino al 23 settembre 2026 il frontend non aveva dipendenze: 21 KB di moduli ES scritti a mano,
nessun bundler, nessun `package.json`. La direttiva di rebase visivo chiede motion, componenti
studiati su 21st.dev e — dove lo meritano — isole React. Ognuna di queste cose porta pacchetti,
e la stessa direttiva vieta il caos: «non installare 3 librerie di animazione, 4 di icone, 2
framework UI». Questo file è il freno: prima di `npm install`, si legge; dopo, si scrive.

Vincoli che nessuna dipendenza può violare:

- **CSP** `script-src 'self'; style-src 'self'` — niente inline, niente CDN, tutto servito da
  `static/`. Un componente che «funziona solo con lo `<style>` inline» non funziona qui.
- **Nessuna risorsa remota**: font, immagini e script vivono nel repository.
- **Django resta il nucleo**: server-rendered, progressive enhancement. Una dipendenza che
  presuppone una SPA è fuori.
- **Budget** (§ 3): il bundle pubblico non supera la cifra scritta qui sotto senza una riga che
  spieghi perché.

---

## 1. Dipendenze di runtime (spedite al browser)

| Pacchetto | Versione | Licenza | Scopo | Peso misurato | Manutenzione |
|---|---|---|---|---|---|
| `motion` | 13.4.1 (fissata) | MIT | Animazione: `animate`, `scroll`, `inView`, `stagger`, `spring`, `hover`, `press`. Successore ufficiale di Framer Motion (motion.dev). Usato **senza React** dove basta. | Bundle reale `static/js/dist/motion.js` (le sette funzioni sopra + i due helper del progetto, tree-shaken con esbuild, minificato): **65,4 KB / 24,0 KB gzip**. Solo animate+scroll+inView+stagger: 62,8 / 23,1. `motion/mini` (solo `animate`, WAAPI): **9,7 KB / 3,9 KB gzip**. | Attiva: 13.4.1 pubblicata il 22–23 settembre 2026; repo motiondivision/motion. |

Punti d'ingresso verificati (`node --input-type=module`):

- `motion` esporta `animate scroll inView stagger spring hover press animateView`;
- `motion/mini` esporta **solo** `animate` — `scroll` e `inView` non ci sono, contrariamente a
  quanto una lettura frettolosa della documentazione fa credere. La prima prova di bundle è
  fallita esattamente lì.

Decisione d'uso: un solo modulo `static/js/src/motion.js` re-esporta ciò che il progetto usa,
così ogni pagina importa dallo stesso posto e il registro sa cosa è in gioco. Nessun file importa
`motion` direttamente.

React e `motion/react`: **non installati**. Entrano solo con una isola che si giustifica per
iscritto (§ 51 della direttiva: scopo, perché Django/vanilla non bastava, dimensione, entry
point, fallback, accessibilità, reduced-motion). Finché quella riga non esiste, non esistono.

## 2. Dipendenze di sviluppo (mai spedite)

| Pacchetto | Versione | Licenza | Scopo | Manutenzione |
|---|---|---|---|---|
| `esbuild` | 0.28.2 (fissata) | MIT | Bundling ESM tree-shaken di `static/js/src/*` → `static/js/dist/*`, minificazione, sourcemap. Scelto al posto di Vite perché non c'è React da servire in dev e un solo binario senza plugin basta; se arriverà un'isola React, Vite si valuta allora, non prima. | Attiva. |
| `@fontsource/ibm-plex-sans`, `@fontsource/ibm-plex-mono` | 5.3.0 (fissate, devDependencies) | OFL 1.1 (i font), MIT (il pacchetto) | Sorgente dei woff2 di IBM Plex Sans 400/500/600 + 400 corsivo e di IBM Plex Mono 400 (latin, latin-ext), copiati in `static/fonts/` da `scripts/fetch_fonts.py --from-fontsource` (design V4, `DESIGN_SYSTEM_V4.md` §4.1). **Non entrano in nessun bundle** e non sono richiesti a runtime: sono una sorgente di file, come l'API di Google per le altre famiglie. | Attive dal 24/09/2026. Aggiornarle = rieseguire `--from-fontsource` e rileggere §6.2 del design system. |

`node_modules/` è ignorato da git; si ripristina con `npm ci` dal `package-lock.json`, che invece
è versionato. Il prodotto del bundle (`static/js/dist/`) **è versionato**: il server di produzione
non ha Node e `collectstatic` deve trovare i file già pronti. Un test verifica che il dist non sia
più vecchio del src.

## 3. Budget

Fissato prima di aggiungere un effetto, come la direttiva chiede (§ 49, § 80):

| Misura | Oggi (prima del rebase) | Budget V2 | Nota |
|---|---:|---:|---|
| JS pubblico, home, trasferito (gzip) | 5,3 KB (`head.js` 0,2 + `main.js` 5,1, misurati) | **≤ 45 KB** | comprende Motion completo (24 KB) + il codice delle firme visive. Oltre, si spiega qui. |
| JS piattaforma, cruscotto (gzip) | 5,3 KB | **≤ 45 KB** | stesso modulo condiviso, caricato una volta. |
| CSS totale (gzip) | da misurare in fase 7 | **≤ 1,25 × oggi** | il nuovo sistema sostituisce `register.css`, non gli si somma. |
| Font | 5 famiglie self-hosted | **≤ 3 famiglie latine + 2 arabe** | vedi DESIGN_SYSTEM_V2. |
| Immagini hero | 0 | AVIF/WebP, ≤ 120 KB per viewport | solo dove la composizione ne guadagna. |
| LCP / CLS / INP | misurati in `docs/STAGING_PERFORMANCE.md` | non peggiori di prima su staging | confronto prima/dopo obbligatorio (§ 79). |

Regole di carico: Motion e le firme visive sono `type="module"` differiti; gli effetti sotto la
piega si caricano al bisogno (`inView`); le animazioni fuori schermo si mettono in pausa;
`prefers-reduced-motion` porta allo stato finale senza transizione.

## 4. Da 21st.dev

Nessun componente installato finora. Ogni componente che entra passa da
`21ST_COMPONENT_DECISIONS.md` e, se porta pacchetti, da una riga qui. Regola della direttiva
§ 70: un componente che chiede pacchetti sproporzionati a un beneficio visivo piccolo si adatta
a mano, non si installa.

## 5. Cronologia

| Data | Cambiamento |
|---|---|
| 2026-09-23 | Creato `package.json`; `motion` 13.4.1 e `esbuild` 0.28.2 fissati; pesi misurati; budget fissato. |
| 2026-09-24 | `@fontsource/ibm-plex-sans` e `@fontsource/ibm-plex-mono` 5.3.0 come devDependencies: sorgente dei font dell'interfaccia V4 (dieci woff2, 184 KB); Fira Sans e Fira Mono ritirati (dieci woff2, 310 KB). `SPRING_SOFT` / `SPRING_SNAPPY` esportate da `static/js/src/motion.js`. |
