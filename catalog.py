from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def category_list():
    '''This method fetches list of catalog available,
    from database.'''
    catalog = session.query(Categories).all()
    #items = session.query(Items).filter_by(category_id=catalog.id)
    return render_template('categorylist.html', categories=catalog)

@app.route('/catalog/<int:category_id>/items/', methods=['GET', 'POST'])
def show_items(category_id):
   '''Show list items available in any category.'''
   category = session.query(Categories).filter_by(id=category_id).one()
   item = session.query(Items).filter_by(category_id=category_id)
   return render_template('itemlist.html', category=category, items=item)

@app.route('/catalog/<int:category_id>/<int:item_id>/', methods=['GET', 'POST'])
def show_item(category_id, item_id):
    '''Return description of item.'''
    item = session.query(Items).filter_by(id=item_id).one()
    return render_template('itemdescription.html', item=item)

@app.route('/category/new/', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        item = Items(name=request.form['name'],
                     description=request.form['description'],
                     category_id=request.form['catalog'])
        session.add(item)
        session.commit()
        flash('new item added')
        return redirect(url_for('category_list'))
    else:
        categorys = session.query(Categories).all()
        return render_template('newitem.html', category_list=categorys)

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

@app.route('/category/<int:category_id>/delete/<int:item_id>/', methods=['POST','GET'])
def delete_item(category_id, item_id):
    print "Inside deleted method"
    item = session.query(Items).filter_by(id=item_id).one()
    print "fetched item"
    if request.method == 'POST':
        print "inside post"
        session.delete(item)
        print "passed here"
        session.commit()
        print "commited"
        return redirect(url_for('category_list'))
    else:
        return render_template('deleteitem.html', category_id=category_id, item=item)

@app.route('/category/<int:category_id>/items/JSON')
def category_list_api(category_id):
    items = session.query(Items).filter_by(category_id=category_id).all()
    return jsonify(Item_list=[i.serialize for i in items])

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
