web: export OPENAI_API_KEY=$(cat .env | grep OPENAI_API_KEY | cut -d= -f2) && gunicorn app:app
