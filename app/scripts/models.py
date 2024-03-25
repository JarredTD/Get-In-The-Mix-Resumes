from app import db


class ResumeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False, index=True)
    last_name = db.Column(db.String(255), nullable=False, index=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
