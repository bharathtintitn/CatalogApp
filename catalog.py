from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categorys/<int:category_id>/')
def category_list(category_id):
    catalog = session.query(Categories).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=catalog.id)
    return render_template('catalog.html', catalog=catalog, items=items)

@app.route('/category/<int:category_id>/new/')
def new_item(category_id):

    return "new"

@app.route('/category/<int:category_id>/edit/<int:item_id>/')
def edit_item(category_id, item_id):
    return "edit"

@app.route('/category/<int:category_id>/delete/<int:item_id>/')
def delete_item(category_id, item_id):
    return "delete"




if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5000)
