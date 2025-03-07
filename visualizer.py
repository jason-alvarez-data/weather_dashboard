import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

class WeatherVisualizer:
    def __init__(self, static_dir="static"):
        self.static_dir = static_dir
        os.makedirs(f"{static_dir}/images", exist_ok=True)

    def create_temperature_chart(self, forecast_data):
        """Create temperature chart"""
        if "error" in forecast_data:
            return None
        
        df = pd.DataFrame(forecast_data["forecast"])
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Create a Plotly figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["datetime"],
            y=df["temperature"],
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='red', width=2),
            hovertemplate='%{y:1f}°C'
        ))

        fig.update_layout(
            title=f"Temperature Forecast for {forecast_data['city']}",
            xaxis_title="Date & Time",
            yaxis_title="Temperature (°C)",
            hovermode="x unified"
        )

        # Save as HTML for interactive viewing
        chart_path = f"{self.static_dir}/temperature_chart.html"
        fig.write_html(chart_path)

        return chart_path
    
    def create_weather_dashboard(self, current_data, forecast_data):
        """Create a comprehensive weather dashboard"""
        if "error" in current_data or "error" in forecast_data:
            return None
        
        # Convert forecast to DataFrame
        df = pd.DataFrame(forecast_data["forecast"])
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Temperature Forecast",
                "Weather Conditions",
                "Wind Speed",
                "Precipitation Probability"
            ),
            specs=[[{"type": "scatter"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )

        # Temperature forecast
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["temperature"],
                mode='lines+markers', 
                name='Temperature (°C)',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )

        # Weather conditions pie chart
        weather_counts = df["weather_main"].value_counts()
        fig.add_trace(
            go.Pie(
                labels=weather_counts.index,
                values=weather_counts.values,
                name='Weather Conditions'
            ),
            row=1, col=2
        )

        # Wind speed bar chart
        fig.add_trace(
            go.Bar(
                x=df["datetime"],
                y=df["wind_speed"],
                name='Wind Speed (m/s)',
                marker_color='blue'
            ),
            row=2, col=1
        )

        # Precipitation probability
        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["probability"],
                mode='lines+markers',
                name='Percipitation (%)',
                line=dict(color='green', width=2)
            ),
            row=2, col=2
        )

        # Update Layout
        fig.update_layout(
            title_text=f"Weather Dashboard for {forecast_data['city']}",
            height=800,
            showlegend=False
        )

        # Save dashboard
        dashboard_path = f"{self.static_dir}/weather_dashboard.html"
        fig.write_html(dashboard_path)

        return dashboard_path