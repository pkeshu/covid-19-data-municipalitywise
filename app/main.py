from flask import Flask, render_template
import requests

app = Flask(__name__)

columns = [
    {
        "field": "name",
        "title": "Municipality Name",
        "sortable": True,
    },
    {
        "field": "case_count",
        "title": "Case Count",
        "sortable": True,
    },
    {
        "field": "district",
        "title": "District",
        "sortable": True,
    }
]


@app.route('/')
def test():
    r = requests.get('https://data.nepalcorona.info/api/v1/covid/summary')
    data_covid = r.json()

    municipality = requests.get('https://data.nepalcorona.info/api/v1/municipals')
    data_municiple = municipality.json()

    district = requests.get('https://data.nepalcorona.info/api/v1/districts')
    data_district = district.json()

    data = []

    for c in data_covid['municipality']['cases']:
        for m in data_municiple:
            for d in data_district:
                if d.get('id') == m.get('district'):
                    if m.get('id') == c.get('municipality'):
                        d = {
                            'name': m.get('title_ne'),
                            'case_count': c.get('count'),
                            'district': d.get('title_ne')
                        }
                        data.append(d)

    return render_template('table_list.html', data=data, columns=columns, title='Municipality wise data')

#
# if __name__ == '__main__':
#     app.run(debug=True, port=5050)
