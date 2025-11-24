import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import time

API_KEY = "12dfbf26f8e492ce902193724cd8ddac"


# --- Pink Sky Color Palette ---
PINK_SKY_BG = "#fff0f5"    # Lavender Blush (Very light pink background)
ROSE_ACCENT = "#e91e63"    # Deep Pink (Used for temperature)
DARK_MAGENTA = "#880e4f"   # Dark Magenta (Used for text and borders)
BUTTON_BG = "#d81b60"      # Deep Rose (Button background)
ERROR_BG = "#f8bbd0"       # Light Error Pink
ERROR_FG = "#c2185b"       # Dark Error Red

def get_weather(city):
    """Fetches weather data from the OpenWeatherMap API."""
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        messagebox.showerror("Configuration Error", "Please replace 'YOUR_API_KEY_HERE' with your actual OpenWeatherMap API key.")
        return None

    # Use 'units=metric' for Celsius, or 'units=imperial' for Fahrenheit.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        # Make the HTTP request to the API
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        # Check for API error response (e.g., city not found)
        if data.get("cod") == "404":
            messagebox.showerror("Error", f"City not found: {city}")
            return None
        
        # Extract required data points
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "temp_feels": data["main"]["feels_like"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"],
        }
        return weather_info

    except requests.exceptions.Timeout:
        messagebox.showerror("Network Error", "The request timed out. Check your internet connection.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"An error occurred during the request: {e}")
    except KeyError as e:
        messagebox.showerror("Data Error", f"Could not parse weather data (Missing key: {e}). API response structure may have changed.")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    
    return None

def search_weather():
    """Handles the button click, fetches data, and updates the GUI."""
    city_name = city_entry.get()
    weather_data = get_weather(city_name)

    if weather_data:
        # Format sunrise/sunset times
        sunrise_time = datetime.fromtimestamp(weather_data['sunrise']).strftime('%H:%M %p')
        sunset_time = datetime.fromtimestamp(weather_data['sunset']).strftime('%H:%M %p')

        # Update Location Label
        location_label.config(text=f"{weather_data['city']}, {weather_data['country']}", 
                              bg=PINK_SKY_BG, fg=DARK_MAGENTA)

        # Update Temperature and Main Condition
        temp_value = f"{weather_data['temp']:.1f}°C"
        desc_value = weather_data['description']
        temp_label.config(text=temp_value, font=('Helvetica', 48, 'bold'), bg=PINK_SKY_BG, fg=ROSE_ACCENT)
        description_label.config(text=desc_value, font=('Helvetica', 16), bg=PINK_SKY_BG, fg=DARK_MAGENTA)

        # Update Details
        details_text = (
            f"Feels Like: {weather_data['temp_feels']:.1f}°C\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Wind Speed: {weather_data['wind_speed']} m/s\n"
            f"Sunrise: {sunrise_time}\n"
            f"Sunset: {sunset_time}"
        )
        details_label.config(text=details_text, bg=PINK_SKY_BG, fg=DARK_MAGENTA)
    else:
        # Clear previous results if city wasn't found or an error occurred
        location_label.config(text="Location Unknown", bg=ERROR_BG, fg=ERROR_FG)
        temp_label.config(text="--°C", font=('Helvetica', 48, 'bold'), bg=ERROR_BG, fg=ERROR_FG)
        description_label.config(text="Enter City to Check", font=('Helvetica', 16), bg=PINK_SKY_BG, fg=DARK_MAGENTA)
        details_label.config(text="", bg=PINK_SKY_BG, fg=DARK_MAGENTA)


# --- GUI Setup ---

# 1. Initialize the main window
root = tk.Tk()
root.title("Python Weather Checker")
root.geometry("400x500")
root.configure(bg=PINK_SKY_BG) # Light pink sky background

# Optional: Style setup for better appearance (uses ttk for some widgets)
try:
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('clam') 
    style.configure("TButton", font=('Helvetica', 12), padding=10, background=BUTTON_BG, foreground="white")
    style.map("TButton", background=[('active', DARK_MAGENTA)])
except ImportError:
    # Fallback if ttk is not available or desired
    pass

# 2. Input Frame
input_frame = tk.Frame(root, bg=PINK_SKY_BG, pady=10)
input_frame.pack(pady=10)

city_entry = tk.Entry(input_frame, 
                      font=('Helvetica', 14), 
                      width=25, 
                      bd=2, 
                      relief=tk.FLAT,
                      bg="white", 
                      fg=DARK_MAGENTA)
city_entry.grid(row=0, column=0, padx=5, ipady=5)

search_button = tk.Button(input_frame, 
                          text="Check Weather", 
                          command=search_weather, 
                          font=('Helvetica', 12, 'bold'), 
                          bg=BUTTON_BG, # Deep Rose button
                          fg="white", 
                          relief=tk.FLAT,
                          activebackground=DARK_MAGENTA,
                          activeforeground="white",
                          padx=10,
                          pady=5)
search_button.grid(row=0, column=1, padx=5)

# Bind <Return> key to the search function for convenience
root.bind('<Return>', lambda event: search_weather())

# 3. Output Display Frame (Centrally located)
output_frame = tk.Frame(root, bg=PINK_SKY_BG, pady=20)
output_frame.pack(expand=True)

# Location Label
location_label = tk.Label(output_frame, 
                          text="Enter a City Above", 
                          font=('Helvetica', 18, 'bold'), 
                          bg=PINK_SKY_BG, 
                          fg=DARK_MAGENTA, 
                          pady=10)
location_label.pack()

# Temperature Label
temp_label = tk.Label(output_frame, 
                      text="--°C", 
                      font=('Helvetica', 48, 'bold'), 
                      bg=PINK_SKY_BG, 
                      fg=ROSE_ACCENT, 
                      pady=10)
temp_label.pack()

# Description Label
description_label = tk.Label(output_frame, 
                             text="Welcome!", 
                             font=('Helvetica', 16), 
                             bg=PINK_SKY_BG, 
                             fg=DARK_MAGENTA, 
                             pady=5)
description_label.pack()

# Details Label (Humidity, Wind, etc.)
details_label = tk.Label(output_frame, 
                         text="", 
                         font=('Helvetica', 12), 
                         justify=tk.LEFT,
                         bg=PINK_SKY_BG, 
                         fg=DARK_MAGENTA, 
                         pady=10)
details_label.pack()

# Start the Tkinter event loop
root.mainloop()