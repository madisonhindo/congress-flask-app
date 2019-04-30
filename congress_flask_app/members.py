from flask import Flask, render_template, redirect, url_for, request
from modules import convert_to_dict, make_ordinal

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import Required

app = Flask(__name__)
application = app 

app.config['SECRET_KEY'] = 'VguhZssWgM'

Bootstrap(app)

members_list = convert_to_dict("flask_rep_info.csv")
state_financial_list = convert_to_dict("state_financial_info.csv")

class SearchForm(FlaskForm):
    state_choice = SelectField('Select from this list')
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'] )
def index():
    state_list = []
    second_state_list = []
    pairs_list = []
    for state in state_financial_list:
        state_list.append(state['state'])
        second_state_list.append(state['state'])
    pairs_list = zip(state_list, second_state_list)

    form = SearchForm()
    form.state_choice.choices = [ (m[0], m[1]) for m in pairs_list ]

    if request.method == "POST":
        state_choice = request.form.get("state_choice").lower()
        return redirect( url_for('state_page', state_id=state_choice ) )
    return render_template('search.html', form=form)

@app.route('/member/<num>')
def detail(num):
    for member in members_list:
        if member['id'] == num:
            member_dict = member
            break
    return render_template('member.html', mem=member_dict, the_title=member_dict['name'])

@app.route('/state/<state_id>')
def state_page(state_id):
    for state in state_financial_list:
        if state['state'].lower() == state_id:
            s = state
            members = select_where_state_is(state_id)
            break
            
    return render_template('state.html', s=s, the_title=state_id, members=members)

def select_where_state_is(state):
    selected_members = []
    for member in members_list:
        if member[' state'].lower() == state:
            selected_members.append(member)

    return selected_members

if __name__ == '__main__':
    app.run(debug=True)