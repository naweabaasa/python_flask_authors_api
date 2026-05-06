from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    pages = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    price_unit = db.Column(db.String(50),nullable=False,default='UGX')
    publication_date = db.Column(db.Date,nullable=False)
    isbn = db.Column(db.String(30),nullable=True,unique=True)
    genre = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(255),nullable=False)
    image = db.Column(db.String(255),nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
    user = db.relationship('Users',backref='books')
    company = db.relationship('Company',backref='books')
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    
    
def __init__(self, title, pages, price, description,price_unit, publication_date, isbn, genre, image, user_id, company_id, user, company):
        super(Book,self).__init__()
        self.title = title
        self.pages = pages
        self.description = description
        self.price = price
        self.user_id = user_id
        self.price_uint =price_unit
        self.publication_date = publication_date
        self.isbn =isbn
        self.genre = genre
        self.image = image
        self.company_id = company_id
        self.user = user
        self.company = company
    
        
def __repr__(self):
        return f"Book{self.title} {self.origin}"
