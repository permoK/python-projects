# Python Flask example for handling the update request and incrementing the number
from flask import Flask, render_template, jsonify
from flask import Response as HttpResponse

app = Flask(__name__)

# Initialize the number
number = 10

@app.route('/')
def index():
    return render_template('index.html', number=number)

@app.route('/update_number')
def update_number():
    global number  # Declare number as global to modify its value
    number += 1    # Increment the number by 1
    return HttpResponse(str(number))

if __name__ == '__main__':
    app.run(debug=True)
