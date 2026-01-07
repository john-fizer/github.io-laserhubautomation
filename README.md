# LaserFlow Automation - GitHub Pages

A modern web interface for laser cutting automation, now deployed as a static site on GitHub Pages.

## Overview

This is a React-based frontend application built with Vite and styled with Tailwind CSS. It displays a dashboard for monitoring laser cutting machines, jobs, and production status.

## Live Demo

Visit the site at: https://john-fizer.github.io/github.io-laserhubautomation/

## Features

- **Dashboard**: Real-time overview of production status, active lasers, and job queue
- **Machines**: Monitor laser machine status and current programs
- **Jobs**: View and manage the job queue with filtering options
- **Responsive Design**: Works on desktop and mobile devices

## Local Development

### Prerequisites

- Node.js 20 or higher
- npm

### Installation

1. Clone the repository:
```bash
git clone https://github.com/john-fizer/github.io-laserhubautomation.git
cd github.io-laserhubautomation
```

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser to `http://localhost:3000`

### Building for Production

Build the static site:
```bash
npm run build
```

The built files will be in the `dist/` directory.

Preview the production build:
```bash
npm run preview
```

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `main` branch. The deployment is handled by GitHub Actions (see `.github/workflows/deploy-pages.yml`).

## Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library
- **React Router** - Client-side routing

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components (Dashboard, Machines, Jobs)
│   ├── lib/            # Utilities and mock API
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── public/             # Static assets
└── dist/               # Build output (generated)
```

## Note on Backend

This is currently a static site using mock data. The original backend/Docker configuration has been disabled. If you need to integrate with a real backend API, modify `frontend/src/lib/api.js` to use axios or fetch instead of the mock data.

## License

MIT
