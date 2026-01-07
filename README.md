# LaserFlow Automation

Web application interface developed for metal fab laser flow automation.

## 🚀 GitHub Pages Deployment

This repository is configured to automatically deploy the frontend to GitHub Pages when code is pushed to the `main` branch.

### Setup Instructions

To enable GitHub Pages deployment, you need to configure the repository settings:

1. **Go to Repository Settings**
   - Navigate to your repository on GitHub
   - Click on **Settings** (top right of the repository)

2. **Enable GitHub Pages**
   - In the left sidebar, click on **Pages** (under "Code and automation")
   - Under **Source**, select **GitHub Actions**
   - Save the changes

3. **Trigger Deployment**
   - Once configured, the deployment workflow will run automatically when you push to `main`
   - You can also manually trigger it from the **Actions** tab

4. **Access Your Site**
   - After successful deployment, your site will be available at:
   - `https://john-fizer.github.io/laser-flow-automation/`

### Deployment Workflow

The deployment is handled by the `.github/workflows/deploy-gh-pages.yml` workflow which:
- Installs dependencies
- Builds the React frontend with Vite
- Deploys the static files to GitHub Pages

### Local Development

To run the frontend locally:

```bash
cd frontend
npm install
npm run dev
```

The development server will start at `http://localhost:3000`

### Building Locally

To build the frontend for production:

```bash
cd frontend
npm install
npm run build
```

The built files will be in the `frontend/dist` directory.

## 📁 Project Structure

- `/frontend` - React frontend application built with Vite
- `/app` - Backend Python application
- `/.github/workflows` - CI/CD workflows

## 🔧 Technologies

- **Frontend**: React, Vite, TailwindCSS, React Router
- **Backend**: Python, FastAPI (or Flask)
- **Deployment**: GitHub Pages for frontend

## 📝 Notes

- The old CI/CD workflow (`.github/workflows/ci-cd.yml`) was configured for Docker and SSH deployment to an external server
- The new workflow (`deploy-gh-pages.yml`) is specifically for GitHub Pages deployment
- The `base` path in `vite.config.js` is set to `/laser-flow-automation/` to match the GitHub Pages URL structure
