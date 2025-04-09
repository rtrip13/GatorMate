# GatorMate - Netlify Deployment

This folder contains the static files needed to deploy the frontend of GatorMate to Netlify.

## Important Configuration Notes

Before deploying, you need to:

1. Deploy the Flask backend to a service that supports Python applications (e.g., Heroku, Railway, Render, etc.)

2. Update the backend URL in the following files:
   - `static/index.html` - Edit the `baseUrl` variable near the top of the file
   - `netlify.toml` - Update the redirect URLs
   - `_redirects` - Update the redirect URLs

## Deploying to Netlify

### Option 1: Deploy via Netlify CLI

1. Install the Netlify CLI:
   ```
   npm install netlify-cli -g
   ```

2. Log in to your Netlify account:
   ```
   netlify login
   ```

3. Initialize a new Netlify site:
   ```
   netlify init
   ```
   
4. Deploy the site:
   ```
   netlify deploy --prod
   ```

### Option 2: Deploy via Netlify UI

1. Go to [Netlify](https://www.netlify.com/) and log in to your account

2. Drag and drop this entire folder to the Netlify UI, or use the "New site from Git" option

3. Follow the prompts to configure your deployment

## Backend Deployment Considerations

The original Flask application provides the following endpoints that need to be hosted separately:

- `/chat` - Handles chat interactions
- `/analyze_journal` - Analyzes journal entries

Make sure your backend implementation handles CORS for cross-origin requests from your Netlify site. 