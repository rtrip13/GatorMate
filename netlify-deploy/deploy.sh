#!/bin/bash

echo "GatorMate Netlify Deployment Helper"
echo "==================================="
echo

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "Netlify CLI not found. Would you like to install it? (y/n)"
    read install_netlify
    
    if [[ $install_netlify == "y" || $install_netlify == "Y" ]]; then
        npm install netlify-cli -g
    else
        echo "Aborting. Netlify CLI is required for deployment."
        exit 1
    fi
fi

# Prompt for backend URL
echo
echo "Enter your backend API URL (e.g., https://your-backend.herokuapp.com):"
read backend_url

echo
echo "Updating configuration files with the backend URL..."

# Update the files
sed -i '' "s|https://your-backend-url.com|$backend_url|g" static/index.html
sed -i '' "s|https://your-backend-url.com|$backend_url|g" netlify.toml
sed -i '' "s|https://your-backend-url.com|$backend_url|g" _redirects

echo "Configuration updated."
echo

# Ask if user wants to deploy now
echo "Do you want to deploy to Netlify now? (y/n)"
read deploy_now

if [[ $deploy_now == "y" || $deploy_now == "Y" ]]; then
    echo
    echo "Logging in to Netlify..."
    netlify login
    
    echo
    echo "Initializing new Netlify site..."
    netlify init
    
    echo
    echo "Deploying to Netlify..."
    netlify deploy --prod
    
    echo
    echo "Deployment complete!"
else
    echo
    echo "Configuration is ready for deployment."
    echo "To deploy manually, run: netlify deploy --prod"
fi

echo
echo "Thank you for using GatorMate!" 