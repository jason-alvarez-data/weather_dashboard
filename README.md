# Weather Dashboard

A Python-based web application that provides weather information and visualizations for cities around the world.

## Features

- Current weather conditions
- 5-day weather forecast
- Interactive visualizations including:
  - Temperature forecast
  - Weather conditions distribution
  - Wind speed chart
  - Precipitation probability
- Historical weather data tracking

## Technologies Used

- **Backend**: Python, Flask
- **Data Processing**: Pandas
- **Visualization**: Matplotlib, Seaborn, Plotly
- **API**: OpenWeatherMap API

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather_dashboard.git
   cd weather_dashboard
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory and add your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter a city name to get weather information and visualizations.

## Deployment

### Deploying to Vercel

This application is configured for deployment on Vercel:

1. Fork or clone this repository to your GitHub account
2. Sign up for a [Vercel account](https://vercel.com/signup) if you don't have one
3. Create a new project on Vercel and import your GitHub repository
4. Add your `OPENWEATHER_API_KEY` as an environment variable in the Vercel project settings
5. Deploy the application

Vercel will automatically build and deploy your application. Once deployed, you'll receive a URL that you can share with others.

## Project Structure

- `app.py`: Main Flask application
- `weather_service.py`: Handles API requests to OpenWeatherMap
- `data_processor.py`: Processes and transforms weather data
- `visualizer.py`: Creates weather visualizations
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, JavaScript, images)
- `data/`: Stored historical weather data

## License

MIT

## Author
Jason Alvarez

## Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Plotly](https://plotly.com/) for interactive visualizations 