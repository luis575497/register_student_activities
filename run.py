from app import app, db
from app.routes.errors import status_401, status_404

if __name__ == '__main__':
    db.create_all()
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()