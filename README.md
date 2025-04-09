# GatorMate

A supportive AI companion for University of Florida students, providing mental health support, physical wellness coaching, and journaling capabilities.

## Deployment Instructions

### Step 1: Deploy the Backend

You have two options for deploying the backend:

#### Option 1: Deploy to Render.com (Recommended)

1. Create an account at [Render.com](https://render.com)
2. Click "New +" and select "Blueprint" or "Web Service"
3. Connect your GitHub repository or upload the code
4. The `render.yaml` file will automatically configure your service
5. Add your `OPENAI_API_KEY` in the environment variables section
6. Deploy the service and note the URL (e.g., https://gatormate-backend.onrender.com)

#### Option 2: Deploy to Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku: `heroku login`
3. Create a new app: `heroku create gatormate-backend`
4. Add your OpenAI API key: `heroku config:set OPENAI_API_KEY=your_key_here`
5. Deploy the app: `git push heroku main`
6. Note the URL Heroku provides (e.g., https://gatormate-backend.herokuapp.com)

### Step 2: Deploy the Frontend to Netlify

1. Navigate to the `netlify-deploy` directory: `cd netlify-deploy`
2. Run the deployment script: `bash deploy.sh`
3. When prompted, enter your backend URL from Step 1
4. Follow the prompts to complete the deployment

## Local Development

To run the app locally:

1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with your OpenAI API key
3. Run the app: `python app.py`
4. The app will be available at http://localhost:5001 