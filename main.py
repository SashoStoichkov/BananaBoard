from flask import Flask, render_template, request

# Create Flask App
app = Flask(__name__)

# Some configurations
app.config['ENV'] = True
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Welcome to BananaBoard!'


if __name__ == '__main__':
    app.run()
