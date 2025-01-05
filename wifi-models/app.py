from flask import Flask, request, render_template, send_file, url_for
import io
import matplotlib
matplotlib.use('Agg')  # Required for headless mode
from matplotlib import pyplot as plt
from wifi_simulation import simulate_wifi_field
import numpy as np

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        room_size = int(request.form.get('room_size', 101))
        frequency = float(request.form.get('frequency', 5.0))
        
        if room_size < 10 or room_size > 500:
            return "Room size must be between 10 and 500", 400
            
        # Select wavelength based on frequency
        wavelength = 6.0 if frequency == 5 else 12.5
            
        # Run simulation
        field = simulate_wifi_field(room_size=room_size, wavelength=wavelength)
        
        # Create plot
        plt.figure(figsize=(10, 8))
        plt.imshow(field, cmap='jet', aspect='equal')
        plt.colorbar(label='Field Strength')
        plt.title(f'WiFi Field Distribution ({frequency}GHz)\nRoom Size: {room_size}x{room_size}cm')
        
        # Save plot to memory
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        plt.close()
        
        return send_file(img_buf, mimetype='image/png')
        
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
