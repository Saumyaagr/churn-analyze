from flask import Flask, render_template, request, url_for
import requests
import urllib3, json
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        cs = request.form['a']
        geo = request.form['b']
        ge = request.form['c']
        te = request.form['d']
        ias = request.form['e']
        ba = request.form['f']

        print(cs,geo,ge,te,ias,ba)
        try:
            cs = float(cs)
            geo = int(geo)
            ge = int(ge)
            te = int(te)
            ias = int(ias)
            ba = float(ba)

        except:
            return render_template('index.html', err_msg='Enter Valid Data')
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = "apikey=" + 'R_w8LZ7r8xY2HBS2g9bXU1F707TPtA7ZrcwhqX3RWXdo' + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        IBM_cloud_IAM_uid = "bx"
        IBM_cloud_IAM_pwd = "bx"
        response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
        print(response)
        iam_token = response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token}
        payload_scoring = {"input_data": [
            {"fields": ['CreditScore', 'Geography', 'Gender', 'Tenure','IsActiveMember','Balance'],
            "values": [[cs, geo, ge, te, ias,ba]]}]}
        response_scoring = requests.post(
            'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/77052966-e7d2-45f8-a8d3-c1efb82f52a2/predictions?version=2020-10-26',
            json=payload_scoring, headers=header)
        print(response_scoring)
        a = json.loads(response_scoring.text)
        print(a)
        pred = a['predictions'][0]['values'][0][0]

        return render_template('index.html', result=pred)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
