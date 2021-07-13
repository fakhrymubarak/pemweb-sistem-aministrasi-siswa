from api import create_app

app = create_app()

@app.route('/')
def welcome():
    return "It works!"

if __name__ == "__main__":
    app.run(debug=True)