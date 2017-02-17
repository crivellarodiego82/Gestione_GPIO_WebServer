import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from flask_table import Table, Col
app = Flask(__name__, template_folder='/var/www/html/gpio/16/')

GPIO.setmode(GPIO.BCM)
chan_list = [16]
GPIO.setwarnings(False)

# Creare un dizionario chiamato pin per memorizzare il numero di pin, il nome e lo stato:
pins = {
   16 : {'name' : 'GPIO 16', 'state' : GPIO.LOW},
   }

# Impostare ogni pin come output e renderlo basso:
for pin in pins:
   GPIO.setup(chan_list, GPIO.OUT)
   GPIO.output(chan_list, GPIO.LOW)

@app.route("/")
def main():
  # Per ogni pin, leggere lo stato e riporlo nel dizionario:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
  # Inserire il dizionario nel dizionario dei dati del modello:
   templateData = {
      'pins' : pins
      }
  # Far passare i dati del modello nel modello main.html e restituirlo a utente
   return render_template('main.html', **templateData)

# La funzione di seguito viene eseguita quando qualcuno richiede un URL con il numero di pin e azione in esso:

@app.route("/<changePin>/<action>")
def action(changePin, action):

   # Convertire il passaggio di URL in un numero intero:

   changePin = int(changePin)

   # Ottenere il nome del dispositivo per il perno essendo cambiato:

   deviceName = pins[changePin]['name']

   # Se la parte azione del URL "on", eseguire il codice rientrato sotto:

   if action == "on":
      # Impostare il pin alto:

      GPIO.output(changePin, GPIO.HIGH)

      # Salvare il messaggio di stato per essere passato nel modello:

      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # Per ogni pin, leggere lo stato pin e riporlo nel dizionario pin:

   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Insieme al dizionario pins, mettere il messaggio nel dizionario dei dati del modello:

   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='10.0.2.30', port=8000, debug=True)
