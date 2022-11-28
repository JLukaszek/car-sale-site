from flask import Flask, render_template, url_for
app = Flask(__name__)

cars = [
    {
        "car_body": "SUVs",
        "car_brand": "BMW",
        "car_model": "X5",
        "mileage": 96700,
        "price": "$14000",
    },
    {
        "car_body": "Coupe",
        "car_brand": "Audi",
        "car_model": "A4",
        "mileage": 198000,
        "price": "$10000",
    },
    {
        "car_body": "Estate",
        "car_brand": "BMW",
        "car_model": "Series 3",
        "mileage": 68600,
        "price": "$11000",
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', cars=cars)


@app.route("/about")
def about():
    return render_template('about.html', title='About Page')


if __name__ == "__main__":
    app.run(debug=True)
