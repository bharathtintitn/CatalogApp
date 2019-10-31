from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def new_item(category_id):
    if request.method == 'POST':
        item = Items(name=request.form['name'],
                     description=request.form['description'],
                     category_id=category_id)
        session.add(item)
        session.commit()
        return redirect(url_for('category_list', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)

@app.route('/category/<int:category_id>/edit/<int:item_id>/', methods=['POST', 'GET'])
def edit_item(category_id, item_id):
    if request.method == 'GET':
        item = session.query(Items).filter_by(id=item_id).one()
        return render_template('edititem.html', category_id=category_id, i=item)
    else:
        item = Items(name=request.form['name'],
                     description=request.form['description'],
                     category_id=category_id)
        session.add(item)
        session.commit()
        return redirect(url_for('category_list', categroy_id=category_id))


    return "edit"

@app.route('/category/<int:category_id>/delete/<int:item_id>/')
def delete_item(category_id, item_id):
    return "delete"


if __name__ == "__main__":

    app.debug = True
    app.run(host='0.0.0.0', port=5000)
