# Anas Gara — DevOps portfolio

A responsive, buildless portfolio with locally hosted fonts and technology icons, original SVG infrastructure illustrations, project filtering, accessible project dialogs, and English/French CV downloads.

The interface uses a charcoal background, cyan and blue accents, Space Grotesk display typography, and Manrope body copy. Body text is 18–21px, with a large name-led hero, framed architecture diagrams, and structured project and credential cards. An animated delivery diagram, one-time scroll entrances and impact counters, sticky navigation, and a reading progress indicator provide motion. Reduced-motion preferences disable decorative animation and reveal transitions.

The credentials section contains the 12 public badges listed on Anas Gara's Credly profile, checked on 30 October 2026. Each card links to its individual earned-badge verification record; provider filters work locally. Official artwork is in `dist/assets/badges/`, and source metadata is in `dist/assets/credentials.json`. Badge artwork belongs to its respective issuer. The Credly snapshot is static and makes no live API requests.

Run `npm run dev` and open http://127.0.0.1:4173. Run `npm run check` for a JavaScript syntax check. The complete deployable site is in `dist/` and can also be hosted on any static hosting service.

Project content is in `dist/app.js`; profile, experience, and contact content are in `dist/index.html`; the complete design and responsive layouts are in `dist/interface.css`. No runtime dependencies, API keys, tracking, or external fonts are required.

Fonts in use: Space Grotesk, Manrope, and IBM Plex Mono (Open Font License), obtained through Google Fonts. Technology icons: Devicon (MIT). Original CV sources are included in `dist/assets/` alongside the formatted PDFs. Portfolio contact uses the email published on the GitHub profile; supplied CVs retain their respective contact details.
