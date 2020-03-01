from flask import Flask,request,redirect,render_template
from mudpp.mudpp import domudpp
from tempfile import NamedTemporaryFile
import json

app = Flask(__name__)
@app.route('/',methods=['GET'])
def upload_form():
    return render_template('prettyprint.html')
    
@app.route('/',methods=['POST'])
def mudpp():
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
        return "filename blank", 400
    if request.content_type == 'application/json':
        try:
            mudjson = request.get_json()
        except:
            return 'JSON not found', 400
        res = domudpp(mudjson)
        return res, 200
    return "no files", 400

# if __name__ == '__main__':
#    app.run(debug=False, port=5000)
