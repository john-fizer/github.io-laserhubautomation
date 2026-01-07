# GitHub Pages Setup Instructions

This document explains how to enable GitHub Pages for this repository.

## Steps to Enable GitHub Pages

1. **Go to Repository Settings**
   - Navigate to your repository: https://github.com/john-fizer/github.io-laserhubautomation
   - Click on "Settings" tab

2. **Navigate to Pages Settings**
   - In the left sidebar, scroll down to "Pages" under "Code and automation"
   - Click on "Pages"

3. **Configure GitHub Pages**
   - Under "Source", select "GitHub Actions" from the dropdown
   - No other configuration is needed - the workflow file will handle the deployment

4. **Trigger the Deployment**
   - Merge this PR to the `main` branch
   - The GitHub Actions workflow will automatically build and deploy the site
   - You can monitor the deployment in the "Actions" tab

5. **Access Your Site**
   - Once deployed, your site will be available at:
   - https://john-fizer.github.io/github.io-laserhubautomation/

## What Happens After Merging

1. The `.github/workflows/deploy-pages.yml` workflow will trigger
2. It will:
   - Install Node.js and dependencies
   - Build the React application
   - Upload the build artifacts to GitHub Pages
   - Deploy to your GitHub Pages site

## Troubleshooting

### If the workflow fails:

1. Check the Actions tab for error messages
2. Verify that GitHub Pages is enabled in repository settings
3. Ensure the repository has Pages permissions enabled

### If the site doesn't load correctly:

1. Check browser console for errors
2. Verify the `base` path in `frontend/vite.config.js` matches your repository name
3. Wait a few minutes - GitHub Pages can take time to propagate

## Making Future Updates

After the initial setup, any push to the `main` branch will automatically rebuild and redeploy the site.

## Local Development

To run the site locally:

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 to see your changes.
