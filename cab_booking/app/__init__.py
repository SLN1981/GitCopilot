from flask import Flask

def create_app():
    from .api import app
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
