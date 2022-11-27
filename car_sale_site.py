from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    car_types = ['SUVs', 'Trucks', 'Sedans', 'Crossovers', 'Coupes', 'Convertibles', 'Sports Cars', 'Luxury', 'Vans']
    return render_template('home.html', car_types=car_types)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)