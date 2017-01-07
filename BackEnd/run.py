from src.Views import *


if __name__ == "__main__":
    host = app.config['HOST']
    port = app.config['PORT']
    app.run(host=host, port=port, threaded=True)
    app.run(processes=10)
