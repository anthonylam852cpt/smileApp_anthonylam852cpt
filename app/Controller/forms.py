from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import postTags, Tag

from app.Model.models import Post

def get_tag():
    return Tag.query.all()

def get_taglabel(theTag):
    return theTag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    body = TextAreaField('Body', [Length(min=1, max=1500)])
    tag =  QuerySelectMultipleField( 'Tag', query_factory=get_tag , get_label=get_taglabel , widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sortForm = SelectField('Sort Form',choices = [(4, 'Date'), (3, 'Title'), (2,'# of likes'), (1,'Happiness level')])
    refresh = SubmitField('Refresh')
    displayonlyme = BooleanField('Display my posts only')