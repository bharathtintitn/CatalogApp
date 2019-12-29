from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogApp"

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #see if user exists, if it doesn't make a new one
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
    #return "The current session state is %s" % state

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


# User helper methods

def create_user(login_session):

    newUser = User(name=login_session['username'], email=login_session['email'],
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
