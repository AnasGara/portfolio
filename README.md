# Anas Gara — DevOps portfolio

A responsive, buildless portfolio with locally hosted fonts and technology icons, original SVG infrastructure illustrations, project filtering, accessible project dialogs, and English/French CV downloads.

The interface uses a charcoal background, cyan and blue accents, Space Grotesk display typography, and Manrope body copy. Body text is 18–21px, with a large name-led hero, framed architecture diagrams, and structured project and credential cards. An animated delivery diagram, one-time scroll entrances and impact counters, sticky navigation, and a reading progress indicator provide motion. Reduced-motion preferences disable decorative animation and reveal transitions.

The credentials section contains the 12 public badges listed on Anas Gara's Credly profile, checked on 30 October 2026. Each card links to its individual earned-badge verification record; provider filters work locally. Official artwork is in `dist/assets/badges/`, and source metadata is in `dist/assets/credentials.json`. Badge artwork belongs to its respective issuer. The Credly snapshot is static and makes no live API requests.

Run `npm run dev` and open http://127.0.0.1:4173. Run `npm run check` for a JavaScript syntax check. The complete deployable site is in `dist/` and can also be hosted on any static hosting service.

English is the main page at `/`; translated French and German versions are at `/fr/` and `/de/`. The language selector preserves the current section. Translations cover page content, navigation, accessible labels, project dialogs, filters, and operational diagrams. Issued credential names and product names retain their official names. English and French CVs remain available on all three versions.

The theme toggle switches between the dark charcoal/cyan design and the original cream/orange light palette with serif accents. The choice is saved locally and applied before rendering on every language route. No cookies or server storage are used.

Dark mode is the default for new visitors. A returning visitor's explicitly selected theme is remembered.

For Vercel, import the repository and use the included `vercel.json`: no framework, dependency installation, or build step is required, and the output directory is `dist`. All three language routes are included. After claiming a temporary deployment, connect the GitHub repository in Vercel to enable deployments from future pushes.

After editing the English page or `content/translations.json`, run `python localize.py` to regenerate the static translated pages and shared locale data. Common interactive UI lives in `dist/i18n.js` and `dist/theme.js`; theme styling is in `dist/theme.css`.

Project content is in `dist/app.js`; profile, experience, and contact content are in `dist/index.html`; the complete design and responsive layouts are in `dist/interface.css`. No runtime dependencies, API keys, tracking, or external fonts are required.

Fonts in use: Space Grotesk, Manrope, and IBM Plex Mono (Open Font License), obtained through Google Fonts. Technology icons: Devicon (MIT). The updated English and French CV sources are included in `dist/assets/` alongside the formatted PDFs. Both CVs use `anasgara7@gmail.com`, list both professional roles as DevOps Engineer, and include German at A1.2. Regenerate the PDFs with `create_cv.py` using a Python environment with ReportLab and pypdf.
