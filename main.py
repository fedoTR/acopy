from flask import Flask, render_template, request, url_for
import similitud

# Indica que se usarán los templates de la carpeta Templates
app = Flask(__name__, template_folder='Templates')

# Define las rutas, por ejemplo, la principal es index.html
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

# Tiene los métodos y también tiene la ruta para el reporte de links
@app.route('/report',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['text']
      return (similitud.returnTable(similitud.report(str(result))))

# Función main que indica el puerto donde se ejecutará la app
if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=5000)
