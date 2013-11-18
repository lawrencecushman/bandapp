from flask import render_template
from flask import Flask, request, send_from_directory
from lxml import etree
from lxml.etree import XMLSyntaxError
from xmlController import xmlIsValid as xmlValidator

#app = Flask(__name__)


@app.route('/')
@app.route('/index')
def landing_page():
    v = xmlValidator(filepath=app.static_folder+'/bands.xml',
                 schemapath=app.static_folder+'/bandSchema.xsd')
    if not v[0] :
        return v[1].message
    else:
        return render_template('index.html',
            page_name = 'Home')


@app.route('/process', methods=['GET','POST'])
def handle_data():
    if request.method == 'POST':
        return "Hello"
    else:
        try:
            new_title = request.args['tit']
            print new_title
            return render_template('index.html',
                                   title=new_title)
        except Exception, e:
            print 'Error'+e.message


@app.route('/destroy')
def destroy_page():
    return render_template('welcome.html',
                           page_name = 'Destroy')


@app.route('/bands.xml')
@app.route('/bandHTMLStylesheet.xsl')
@app.route('/bandsStylesheet.css')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


#if __name__ == '__main__':
#    app.run()
