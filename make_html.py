#!/usr/bin/env python

import math
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
            l += tags.td(tags.b('Tasks'))
            l += tags.td(tags.b('Dataset Types'))
            l += tags.td(tags.b('Attribute Types'))
            l += tags.td(tags.b('Area'))
            l += tags.td(tags.b('Hits'))
            l += tags.td(tags.b('Date'))

        with tags.tbody():
            for item in data:
                l = tags.tr()
                l += tags.td(tags.a(item['name'], href=item['url']))
                l += tags.td(clean_na(item['instances']))
                l += tags.td(clean_na(item['attributes']))
                l += tags.td(item['missings'])
                l += tags.td(item['tasks'])
                l += tags.td(item['dset_characteristics'])
                l += tags.td(item['attr_characteristics'])
                l += tags.td(item['area'])
                l += tags.td(clean_na(item['hits']))
                l += tags.td(item['date'])

    return table

def field_minmax(data, field):
    i, a = 0, 0
    for item in data:
        if not isinstance(item[field], int):
            continue
        i = min(i, item[field])
        a = max(a, item[field])
    return i, a


def field_uniq(data, field, split=False):
    s = set()
    for item in data:
        if split:
            for val in item[field].split(','):
                s.add(val.strip())
        else:
            s.add(item[field])
    return sorted(s)


def add_menu(data):
    inst_min, inst_max = field_minmax(data, 'instances')
    with tags.div(cls='ui', id='instance_ui') as div:
        div += tags.b('Number of instances:')
        div += tags.br()
        div += "Min: "
        div += tags.input(min=str(inst_min), max=str(inst_max),
                cls="i-val", id="inst-min", value=str(inst_min),
                size=math.ceil(math.log(inst_max, 10)))
        div += tags.br()
        div += "Max: "
        div += tags.input(min=str(inst_min), max=str(inst_max),
                cls="i-val", id="inst-max", value=str(inst_max),
                size=math.ceil(math.log(inst_max, 10)))

    attr_min, attr_max = field_minmax(data, 'attributes')
    with tags.div(cls='ui', id='attribute_ui') as div:
        div += tags.b('Number of attributes:')
        div += tags.br()
        div += "Min: "
        div += tags.input(min=str(attr_min), max=str(attr_max),
                cls="a-val", id="attr-min", value=str(attr_min),
                size=math.ceil(math.log(attr_max, 10)))
        div += tags.br()
        div += "Max: "
        div += tags.input(min=str(attr_min), max=str(attr_max),
                cls="a-val", id="attr-max", value=str(attr_max),
                size=math.ceil(math.log(attr_max, 10)))

    dominate.util.raw("The following menus add rows that match <i>any</i>"
            " of the selected items.")

    with tags.div(cls='ui', id='missing_ui') as div:
        div += tags.b('Missing values:')
        div += tags.br()
        with tags.select(id='missing-select', multiple='') as sel:
            for field in field_uniq(data, 'missings'):
                sel += tags.option(field, value=field)

    with tags.div(cls='ui', id='task_ui') as div:
        div += tags.b('Tasks:')
        div += tags.br()
        with tags.select(id='task-select', multiple='') as sel:
            for field in field_uniq(data, 'tasks', split=True):
                sel += tags.option(field, value=field)

    with tags.div(cls='ui', id='dset_type_ui') as div:
        div += tags.b('Dataset Types:')
        div += tags.br()
        with tags.select(id='dset-select', multiple='') as sel:
            for field in field_uniq(data, 'dset_characteristics', split=True):
                sel += tags.option(field, value=field)

    with tags.div(cls='ui', id='attr_type_ui') as div:
        div += tags.b('Attribute Types:')
        div += tags.br()
        with tags.select(id='attr-select', multiple='') as sel:
            for field in field_uniq(data, 'attr_characteristics', split=True):
                sel += tags.option(field, value=field)

    with tags.div(cls='ui', id='area_ui') as div:
        div += tags.b('Area:')
        div += tags.br()
        with tags.select(id='area-select', multiple='') as sel:
            for field in field_uniq(data, 'area'):
                sel += tags.option(field, value=field)




def main():
    data = get_data()

    doc = dominate.document(title=dominate.util.raw(
        'GjjvdBurg &middot; UCI Datasets Filter'))

    with doc.head:
        tags.link(rel='stylesheet', 
                href=('https://cdn.datatables.net/1.10.11/css/'
                    'jquery.dataTables.min.css'))
        tags.link(rel='stylesheet', href='./chosen.min.css')
        with tags.style(type='text/css') as style:
            style.add(
                    "#body {\n"
                    "\twidth: 95%;\n"
                    "\theight: 95%;\n"
                    "\tpadding-bottom: 10px;\n"
                    "}\n"
                    "#menu {\n"
                    "\tpadding-top: 20px;\n"
                    "\twidth: 20%;\n"
                    "\tfloat: left;\n"
                    "}\n"
                    "#table { width: 80%; float: left; }\n"
                    "#header {\n"
                    "\ttext-align: center;\n"
                    "}\n"
                    "#footer {\n"
                    "\tposition: absolute;\n"
                    "\tbottom: 0;\n"
                    "\tleft: 0;\n"
                    "\twidth: 100%;\n"
                    "\ttext-align: center;\n"
                    "}\n"
                    ".ui {\n"
                    "\tmargin: 10pt 5pt 10pt 5pt;\n"
                    "}"
                    )
        tags.script(type='text/javascript',
                src='https://code.jquery.com/jquery-1.12.0.min.js')
        tags.script(type='text/javascript',
                src=('https://cdn.datatables.net/1.10.11/js/'
                    'jquery.dataTables.min.js'))
        tags.script(type='text/javascript', src='./chosen.jquery.min.js')

        with tags.script(type='text/javascript') as script:
            script.add(dominate.util.raw("\n$(document).ready(function() {\n"
                    "var thetable = $('#uci_table').DataTable({\n"
                    "dom: 'lrtpi',\n"
                    "scrollCollapse: true,\n"
                    "scrollY: '80vh',\n"
                    "scrollX: '100%%',\n"
                    "paging: false,\n"
                    "});\n"
                    "var iMin = document.getElementById('inst-min');\n"
                    "var iMax = document.getElementById('inst-max');\n"
                    "var aMin = document.getElementById('attr-min');\n"
                    "var aMax = document.getElementById('attr-max');\n"
                    "$.fn.dataTable.ext.search.push(\n"
                    "function (settings, data, dataIndex) {\n"
                    "var imin = parseInt( iMin.value, 10);\n"
                    "var imax = parseInt( iMax.value, 10);\n"
                    "var inst = parseFloat( data[1] ) || 0;\n"
			        "if (! ( ( isNaN( imin ) && isNaN( imax ) ) ||\n"
			        "    ( isNaN( imin ) && inst <= imax ) ||\n"
			        "    ( imin <= inst   && isNaN( imax ) ) ||\n"
			        "    ( imin <= inst   && inst <= imax ) ) )\n"
			        "{ return false; }\n"
                    "var amin = parseInt( aMin.value, 10);\n"
                    "var amax = parseInt( aMax.value, 10);\n"
                    "var attr = parseFloat( data[2] ) || 0;\n"
			        "if (! ( ( isNaN( amin ) && isNaN( amax ) ) ||\n"
			        "    ( isNaN( amin ) && inst <= amax ) ||\n"
			        "    ( amin <= attr   && isNaN( amax ) ) ||\n"
			        "    ( amin <= attr   && attr <= amax ) ) )\n"
			        "{ return false; }\n"
                    "var miss = $('#missing-select').chosen().val();\n"
                    "var isin = false;\n"
                    "if (miss === null) { isin = true; }\n"
                    "for (idx in miss) {\n"
                    "\tif ( data[3].indexOf(miss[idx]) > -1) {\n"
                    "\t\tisin = true; }\n"
                    "}\nif (isin == false) { return isin; }\n"
                    "var task = $('#task-select').chosen().val();\n"
                    "isin = false;\n"
                    "if (task === null) { isin = true; }\n"
                    "for (idx in task) {\n"
                    "\tif ( data[4].indexOf(task[idx]) > -1) {\n"
                    "\t\tisin = true; }\n"
                    "}\nif (isin == false) { return isin; }\n"
                    "var dset = $('#dset-select').chosen().val();\n"
                    "isin = false;\n"
                    "if (dset === null) { isin = true; }\n"
                    "for (idx in dset) {\n"
                    "\tif ( data[5].indexOf(dset[idx]) > -1) {\n"
                    "\t\tisin = true; }\n"
                    "}\nif (isin == false) { return isin; }\n"
                    "var attr = $('#attr-select').chosen().val();\n"
                    "isin = false;\n"
                    "if (attr === null) { isin = true; }\n"
                    "for (idx in attr) {\n"
                    "\tif ( data[6].indexOf(attr[idx]) > -1) {\n"
                    "\t\tisin = true; }\n"
                    "}\nif (isin == false) { return isin; }\n"
                    "var area = $('#area-select').chosen().val();\n"
                    "isin = false;\n"
                    "if (area === null) { isin = true; }\n"
                    "for (idx in area) {\n"
                    "\tif ( data[7].indexOf(area[idx]) > -1) {\n"
                    "\t\tisin = true; }\n"
                    "}\nreturn isin;\n"
                    "});\n"
                    "iMin.addEventListener('change', function() {\n"
                    "\tthetable.draw();\n"
                    "});\n"
                    "iMax.addEventListener('change', function() {\n"
                    "\tthetable.draw();\n"
                    "});\n"
                    "aMin.addEventListener('change', function() {\n"
                    "\tthetable.draw();\n"
                    "});\n"
                    "aMax.addEventListener('change', function() {\n"
                    "\tthetable.draw();\n"
                    "});\n"
                    "$('#missing-select').chosen({width: '90%'}).change(\n"
                    "function() { thetable.draw(); });\n"
                    "$('#task-select').chosen({width: '90%'}).change(\n"
                    "function() { thetable.draw(); });\n"
                    "$('#dset-select').chosen({width: '90%'}).change(\n"
                    "function() { thetable.draw(); });\n"
                    "$('#attr-select').chosen({width: '90%'}).change(\n"
                    "function() { thetable.draw(); });\n"
                    "$('#area-select').chosen({width: '90%'}).change(\n"
                    "function() { thetable.draw(); });\n"
                  "} );"))
    with doc:
        with tags.div(id='header') as div:
            div += tags.b('Filter the UCI repository datasets.')

        with tags.div(id='body'):
            with tags.div(id='menu'):
                add_menu(data)
            with tags.div(id='table'):
                add_table(data)

        with tags.div(id='footer') as div:
           div += dominate.util.raw("Created by "
            "<a href='https://github.com/GjjvdBurg/'>@GjjvdBurg</a>"
            " using <a href='http://scrapy.org/'>Scrapy</a>, "
            "<a href='https://github.com/Knio/dominate'>dominate</a>, "
            "<a href='https://www.datatables.net/'>DataTables</a>, "
            "and <a href='https://github.com/harvesthq/chosen'>Chosen</a>. "
            "Data scraped from the "
            "<a href='https://archive.ics.uci.edu/ml/datasets.html'>"
            "UCI repository</a>. Code on "
            "<a href='https://github.com/GjjvdBurg/UCI_Datasets_Filter'>"
            "GitHub</a>.")

    with open('index.html', 'w') as fid:
        fid.write(str(doc))


if __name__ == '__main__':
    main()
