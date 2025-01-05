from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            L = int(request.form['length'])
            frequency = float(request.form['frequency'])
            app.logger.debug(f"Received input - Length: {L}, Frequency: {frequency}")
            
            lamda = 300 / frequency  # Speed of light / frequency
            Lsquared = L**2
            KnotSquared = (2*np.pi/lamda)**2

            Rx = L-5
            Ry = Rx

            room = np.zeros([L,L])
            EquationMatrix = np.zeros([Lsquared, Lsquared])
            JMatrix = np.zeros([Lsquared,1])
            JMatrix[Rx*L+Ry]  = 1

            for i in range(L):  
                for j in range(L):
                    index = i*L + j
                    if i > 0:
                        EquationMatrix[index, index - L] = 1
                    if i < L - 1:
                        EquationMatrix[index, index + L] = 1
                    if j > 0:
                        EquationMatrix[index, index - 1] = 1
                    if j < L - 1:
                        EquationMatrix[index, index + 1] = 1
                    EquationMatrix[index, index] = -4 + KnotSquared

            EfieldMatrix = np.linalg.solve(EquationMatrix, JMatrix)
            app.logger.debug("Solved the equation matrix")

            for x in range(L):
                for y in range(L):
                    room[x,y] = EfieldMatrix[x*L + y]

            plt.figure()          
            plt.imshow(room, cmap='jet')
            plt.colorbar()
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            app.logger.debug("Generated the plot")

            return render_template('index.html', plot_url=plot_url)
        except Exception as e:
            app.logger.error(f"Error during simulation: {e}")
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
