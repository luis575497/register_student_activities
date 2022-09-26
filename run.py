from app import app, db
from app.routes.errors import status_401, status_404

if __name__ == "__main__":
    db.create_all()
    app.run()
