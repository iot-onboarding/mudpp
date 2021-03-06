from flask import Flask,request,redirect,render_template
from mudpp.mudpp import domudpp
from tempfile import NamedTemporaryFile
import json, requests

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/',methods=['GET'])
@app.route('/mudpp',methods=['GET'])
@app.route('/mudpp/',methods=['GET'])
def upload_form():
    return render_template('prettyprint.html')
    
@app.route('/betapp',methods=['GET'])
@app.route('/betapp/',methods=['GET'])
def upload_bform():
    return render_template('betaprint.html')

@app.route('/mudpp',methods=['POST'])
@app.route('/mudpp/',methods=['POST'])
def mudpp():
    rtype=request.form.get('intype')
    if rtype == 'file':
        if request.files:
            mudfile=request.files['mudfile']
            if mudfile.filename != '':
                tempfile=NamedTemporaryFile(delete=False)
                mudfile.save(tempfile.name)
                tempfile.seek(0)
                try:
                    mudjson=json.load(tempfile)
                    res=domudpp(mudjson)
                    return res, 200
                except:
                    return 'Unable to load JSON file', 400
    if rtype == 'mudurl':
        mudurl=request.form.get('mudurl')
        if mudurl != None:
            try:
                mudjson=json.loads(requests.get(mudurl).text)
                res=domudpp(mudjson)
                return res, 200
            except:
                return "Something went wrong with URL", 400

    if request.content_type == 'application/json':
        try:
            mudjson = request.get_json()
        except:
            return 'JSON not found', 400
        res = domudpp(mudjson)
        return res, 200
    res="Not sure what I got: " + request.get_data(as_text=True)
    return res, 400

# if __name__ == '__main__':
#    app.run(debug=False, port=5000)
