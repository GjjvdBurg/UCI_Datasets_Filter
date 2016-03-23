#!/usr/bin/env python

import json
import dominate
from dominate import tags

JSON_FILE = './uci/items.jl'

def get_data():
    data = []
    with open(JSON_FILE, 'r') as fid:
        for line in fid:
            data.append(json.loads(line))
    return data


def clean_na(x):
    if x == 'N/A':
        return '-'
    return x


def add_table(data):
    with tags.table(id='uci_table', cls='display', width='100%', 
            cellspacing='0') as table:
        with tags.thead():
            l = tags.tr()
            l += tags.td(tags.b('Name'))
            l += tags.td(tags.b('Instances'))
            l += tags.td(tags.b('Attributes'))
            l += tags.td(tags.b('Missing Values'))
            l += tags.td(tags.b('Date'))
            l += tags.td(tags.b('Dataset Types'))
            l += tags.td(tags.b('Attribute Types'))
            l += tags.td(tags.b('Hits'))
            l += tags.td(tags.b('Area'))
            l += tags.td(tags.b('Tasks'))

        with tags.tbody():
            for item in data:
                l = tags.tr()
                l += tags.td(tags.a(item['name'], href=item['url']))
                l += tags.td(clean_na(item['instances']))
                l += tags.td(clean_na(item['attributes']))
                l += tags.td(clean_na(item['missings']))
                l += tags.td(clean_na(item['date']))
                l += tags.td(clean_na(item['dset_characteristics']))
                l += tags.td(clean_na(item['attr_characteristics']))
                l += tags.td(clean_na(item['hits']))
                l += tags.td(clean_na(item['area']))
                l += tags.td(clean_na(item['tasks']))

    return table


def add_menu():
    with tags.div(id='instance_ui') as div:
        div += tags.b('Number of instances:')
        div += tags.div(id='islider')
        div += tags.br()
        div += "Min: "
        div += tags.input(cls="i-val", id="islider-value-min")
        div += tags.br()
        div += "Max: "
        div += tags.input(cls="i-val", id="islider-value-max")

    with tags.div(id='attribute_ui') as div:
        div += tags.b('Number of attributes:')
        div += tags.div(id='aslider')
        div += tags.br()
        div += "Min: "
        div += tags.input(cls="a-val", id="aslider-value-min")
        div += tags.br()
        div += "Max: "
        div += tags.input(cls="a-val", id="aslider-value-max")


def field_minmax(data, field):
    i, a = 0, 0
    for item in data:
        if not isinstance(item[field], int):
            continue
        i = min(i, item[field])
        a = max(a, item[field])
    return i, a


def main():
    data = get_data()

    doc = dominate.document(title='UCI Datasets Overview')

    with doc.head:
        tags.link(rel='stylesheet', 
                href=('https://cdn.datatables.net/1.10.11/css/'
                    'jquery.dataTables.min.css'))
        tags.link(rel='stylesheet', href='nouislider.min.css')
        with tags.style(type='text/css') as style:
            style.add("#body { width: 95%; }\n"
                    "#menu { width: 20%; float: left; overflow: hidden; }\n"
                    "#table { width: 80%; float: left; overflow: hidden; }\n")
        tags.script(type='text/javascript', src='nouislider.min.js')
        tags.script(type='text/javascript',
                src='https://code.jquery.com/jquery-1.12.0.min.js')
        tags.script(type='text/javascript',
                src=('https://cdn.datatables.net/1.10.11/js/'
                    'jquery.dataTables.min.js'))

        inst_min, inst_max = field_minmax(data, 'instances')
        attr_min, attr_max = field_minmax(data, 'attributes')


        with tags.script(type='text/javascript') as script:
            script.add(dominate.util.raw("\n$(document).ready(function() {\n"
                    "\tvar thetable = $('#uci_table').DataTable({\n"
                    "dom: 'lrtpi',\n"
                    "scrollCollapse: true,\n"
                    "scrollY: '80vh',\n"
                    "scrollX: '100%%',\n"
                    "paging: false,\n"
                    "});\n"
                    "var isldr = document.getElementById('islider');\n"
                    "noUiSlider.create(isldr, {\n"
                    "start: [%i, %i],\n"
                    "connect: true,\n"
                    "range: {\n"
                    "\t'min': %i,\n"
                    "\t'20%%': [100, 50],\n"
                    "\t'70%%': [1e4, 500],\n"
                    "\t'90%%': [1e5, 1000],\n"
                    "\t'max': %i\n"
                    "}\n"
                    "});\n"
                    "var asldr = document.getElementById('aslider');\n"
                    "noUiSlider.create(asldr, {\n"
                    "start: [%i, %i],\n"
                    "connect: true,\n"
                    "range: {\n"
                    "\t'min': [%i, 1],\n"
                    "\t'30%%': [10, 10],\n"
                    "\t'85%%': [100, 100],\n"
                    "\t'max': %i,\n"
                    "}\n"
                    "});\n"
                    "$.fn.dataTable.ext.search.push(\n"
                    "function (settings, data, dataIndex) {\n"
                    "var ivals = isldr.noUiSlider.get();\n"
                    "var avals = asldr.noUiSlider.get();\n"
                    "var imin = parseInt( ivals[0], 10);\n"
                    "var imax = parseInt( ivals[1], 10);\n"
                    "var amin = parseInt( avals[0], 10);\n"
                    "var amax = parseInt( avals[1], 10);\n"
                    "var inst = parseFloat( data[1] ) || 0;\n"
                    "var attr = parseFloat( data[2] ) || 0;\n"
			        "if (! ( ( isNaN( imin ) && isNaN( imax ) ) ||\n"
			        "    ( isNaN( imin ) && inst <= imax ) ||\n"
			        "    ( imin <= inst   && isNaN( imax ) ) ||\n"
			        "    ( imin <= inst   && inst <= imax ) ) )\n"
			        "{ return false; }\n"
			        "else if (! ( ( isNaN( amin ) && isNaN( amax ) ) ||\n"
			        "    ( isNaN( amin ) && inst <= amax ) ||\n"
			        "    ( amin <= attr   && isNaN( amax ) ) ||\n"
			        "    ( amin <= attr   && attr <= amax ) ) )\n"
			        "{ return false; } return true;\n"
                    "});\n"
                    "var iMin = document.getElementById('islider-value-min');\n"
                    "var iMax = document.getElementById('islider-value-max');\n"
                    "isldr.noUiSlider.on('update', function(values, handle) {\n"
                    "if (handle) { iMax.value = values[handle]; }\n"
                    "else { iMin.value = values[handle]; }\n"
                    "thetable.draw();\n"
                    "});\n"
                    "iMin.addEventListener('change', function() {\n"
                    "\tisldr.noUiSlider.set([this.value, null]); });\n"
                    "iMax.addEventListener('change', function() {\n"
                    "\tisldr.noUiSlider.set([null, this.value]); });\n"
                    "var aMin = document.getElementById('aslider-value-min');\n"
                    "var aMax = document.getElementById('aslider-value-max');\n"
                    "asldr.noUiSlider.on('update', function(values, handle) {\n"
                    "if (handle) { aMax.value = values[handle]; }\n"
                    "else { aMin.value = values[handle]; }\n"
                    "thetable.draw();\n"
                    "});\n"
                    "aMin.addEventListener('change', function() {\n"
                    "\tasldr.noUiSlider.set([this.value, null]); });\n"
                    "aMax.addEventListener('change', function() {\n"
                    "\tasldr.noUiSlider.set([null, this.value]); });\n"
                 "} );" % (inst_min, inst_max, inst_min, inst_max,
                    attr_min, attr_max, attr_min, attr_max)))

    with doc:
        with tags.div(id='header'):
            pass

        with tags.div(id='body'):
            with tags.div(id='menu'):
                add_menu()
            with tags.div(id='table'):
                add_table(data)

        with tags.div(id='footer'):
            pass

    with open('index.html', 'w') as fid:
        fid.write(str(doc))


if __name__ == '__main__':
    main()
