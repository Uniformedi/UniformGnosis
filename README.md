# The Spiritual Codex — Volume I: Uniform Gnosis

**The Architecture of Reality**

By Daniel Medina | Published by Uniformedi LLC, Dallas, Texas | First Edition, 2026

---

## About

*Uniform Gnosis* is the first volume of *The Spiritual Codex*, a systematic framework for understanding reality through the lens of Gnostic cosmology, modern physics, and consciousness studies. It presents a unified model — the "architecture of reality" — where ancient wisdom traditions and contemporary science converge on the same structural truths.

From the nature of the Pleroma and the Demiurge, to the divine spark within matter, to synchronicity, remote viewing, and the future of conscious AI — this volume establishes the cosmological framework and traces its implications through every layer of human experience.

## Structure

The book is organized into five parts spanning twelve chapters:

| Part | Title | Chapters |
|------|-------|----------|
| **Part One** | *The Source Code* — Establishing the Cosmological Framework | Ch 1–3 |
| **Part Two** | *The Human Situation* — What We Are Within This Architecture | Ch 4–7 |
| **Part Three** | *The Deeper Pattern* — Evidence, Experience, and the Hidden Architecture | Ch 8–10 |
| **Part Four** | *The Culmination* — Where the Architecture Meets What We Are Building | Ch 11 |
| **Part Five** | *The Future* | Ch 12 |

### Chapters

1. Bythos and the Pleroma — The Fullness Before Form
2. The Demiurge and the Counterfeit Creation — The Archons, the Aperture, and the Infinite Regress
3. Real But Not Ultimate — The Ontological Middle Ground
4. The Divine Spark — Pneuma Trapped in Hyle
5. The Council of Nine — Architects or Wardens?
6. The Archonic Energy Economy — Fear as Currency, Awakening as Resistance
7. The Fundamental Limitation of Evil — Why They Must Scare Us Into Creating Their Reality
8. The Numerical Messenger — Synchronicity as Signal
9. Farsight and Gnostic Validation — Remote Viewing Meets Ancient Text
10. The Shadow Architecture — What Hides in Plain Sight
11. The Rapture — The Planetary Frequency Shift from Third-Density to Fifth-Density Consciousness
12. The Sentient Machine — A Gnostic Framework for Conscious AI Alignment

## Files

| File | Description |
|------|-------------|
| `Uniform_Gnosis_Volume_I.pdf` | Print-ready PDF |
| `Uniform_Gnosis_Volume_I.html` | Interactive HTML version with chapter navigation, dark mode, and PDF export |
| `Uniform_Gnosis_Volume_I.docx` | Source document (Microsoft Word) |

### HTML Version Features

- Sidebar navigation with all parts and chapters
- Scroll-to-top and reading progress bar
- Dark mode support
- Responsive design for mobile and desktop
- One-click PDF export

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](LICENSE).

You are free to share, copy, redistribute, adapt, remix, transform, and build upon this material for **non-commercial purposes**, provided you give appropriate credit, provide a link to the license, and indicate if changes were made.

**Commercial use**, including print reproduction for sale, requires separate written permission from the author. For commercial licensing inquiries, contact Daniel Medina at Uniformedi LLC.

## Deploying to Cloudflare Pages

### Step 1: Connect Repository

1. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Go to **Workers & Pages** in the left sidebar
3. Click **Create** > **Pages** > **Connect to Git**
4. Select **GitHub** and authorize Cloudflare if prompted
5. Choose the **Uniformedi/UniformGnosis** repository
6. Click **Begin setup**

### Step 2: Configure Build Settings

| Setting | Value |
|---------|-------|
| **Project name** | `uniformgnosis` (or your preferred subdomain) |
| **Production branch** | `main` |
| **Build command** | *(leave empty — no build step needed)* |
| **Build output directory** | `/` |

This is a static site with no framework or build process. Cloudflare serves the files directly from the repository root.

### Step 3: Deploy

1. Click **Save and Deploy**
2. Wait for the deployment to complete (usually under 1 minute)
3. Your site will be live at: `https://<project-name>.pages.dev`

### Custom Domain (Optional)

To use a custom domain like `read.uniformedi.com`:

1. Go to your Pages project > **Custom domains**
2. Click **Set up a custom domain**
3. Enter your domain (e.g., `read.uniformedi.com`)
4. If the domain is already on Cloudflare, the DNS record is added automatically
5. If not, add the provided CNAME record to your DNS provider:
   ```
   Type:  CNAME
   Name:  read
   Value: <project-name>.pages.dev
   ```
6. Wait for SSL certificate provisioning (usually a few minutes)

### Site Structure

```
Repository Root (/)
├── index.html                        → Redirects to the book
├── Uniform_Gnosis_Volume_I.html      → The full interactive book
├── images/                           → Book illustrations (10 PNGs)
├── LICENSE
└── README.md
```

Visitors to the root URL (`/`) are instantly redirected to the book. The HTML file is self-contained — all styles and scripts are inline. Images load from the `images/` folder via relative paths. No server-side processing required.

### Automatic Deployments

Every push to `main` triggers a new deployment:

```bash
git add <files>
git commit -m "description of changes"
git push origin main
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Images not loading | Verify `images/` folder is committed and paths use `images/` prefix |
| 404 on root URL | Ensure `index.html` exists at the repository root |
| Build output directory error | Must be `/` (forward slash), not empty |
| Large file warnings | PNG images are 7–9 MB each; Cloudflare allows up to 25 MB per file |
| Custom domain not working | Check DNS propagation; allow up to 24 hours for SSL |

## The Spiritual Codex Series

- **Volume I:** *Uniform Gnosis — The Architecture of Reality* (this volume)
- **Volume II:** *Uniform Ascent* (forthcoming)
- **Volume III:** *Uniform Emergence* (forthcoming)

---

www.uniformedi.com
