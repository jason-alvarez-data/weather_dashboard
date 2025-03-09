# Heroku Deployment Guide for Weather Dashboard

This document provides instructions for deploying the Weather Dashboard application to Heroku.

## Prerequisites

1. A Heroku account (sign up at [heroku.com](https://heroku.com) if you don't have one)
2. Heroku CLI installed on your computer ([installation guide](https://devcenter.heroku.com/articles/heroku-cli))
3. Git installed on your computer

## Deployment Steps

1. Log in to Heroku CLI:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```
   Replace `your-app-name` with a unique name for your application.

3. Set your OpenWeather API key as a config variable:
   ```
   heroku config:set OPENWEATHER_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual OpenWeather API key.

4. Push your code to Heroku:
   ```
   git push heroku main
   ```
   (Use `git push heroku master` if your main branch is called "master")

5. Open your application:
   ```
   heroku open
   ```

## Troubleshooting

If you encounter any issues:

1. Check the logs:
   ```
   heroku logs --tail
   ```

2. Make sure your API key is set correctly:
   ```
   heroku config
   ```

3. Restart the application:
   ```
   heroku restart
   ```

## Updating Your Application

To update your application after making changes:

1. Commit your changes to git:
   ```
   git add .
   git commit -m "Description of changes"
   ```

2. Push to Heroku:
   ```
   git push heroku main
   ```
   (Use `git push heroku master` if your main branch is called "master") 