import datetime

from flask import Flask, Blueprint, jsonify, redirect
from flask.ext.login import current_user
from flask.templating import render_template

from capteur import Capteur
from extensions import db
from .models import Graphique, Colonne, agregats_name

bp_graphique = Blueprint('graphique_bp',__name__, static_folder='../static')


@bp_graphique.route('/graph/json/user')
def user_graph(id):
    return redirect('/graph/json/' + current_user.graphiques.graphId)


@bp_graphique.route('/graph/add/<int:id>/<int:captId>')
def add_column(id, captId):
    graph = Graphique.query.get(id)
    capt = Capteur.query.get(captId)
    c = Colonne(graphique=graph,
                colName=capt.cName,
                capteur=capt,
                )
    db.session.add(c)
    db.session.commit()
    return graph_json(id)

@bp_graphique.route('/graph/add/<int:id>/<int:captId>/')
@bp_graphique.route('/graph/add/<int:id>/<int:captId>/<string:agregat>')
def add_column_agregat(id, captId, agregat=""):
    graph = Graphique.query.get(id)
    capt = Capteur.query.get(captId)
    colname = capt.cName
    if agregat: colname += ' : ' + agregats_name[agregat]
    c = Colonne(graphique=graph,
                colName=colname,
                capteur=capt,
                agregatSimple=agregat,
                )
    db.session.add(c)
    db.session.commit()
    return graph_json(id)


@bp_graphique.route('/graph/delete/<int:id>/<int:captId>')
def delete_column(id, captId):
    c = Colonne.query.filter_by(graphique=Graphique.query.get(id)).filter_by(capteur=Capteur.query.get(captId)).first()
    db.session.delete(c)
    db.session.commit()
    return graph_json(id)


@bp_graphique.route('/graph/json/<int:id>')
def graph_json(id):
    graph = Graphique.query.get(id)
    ans = {
        'id': graph.graphId,
        'chart': {
            'zoomType': 'x'
        },
        'series': [{
            'data': serie.valeurs_datees,
            'name': serie.colName
        } for serie in graph.colonnes],
        'title': {
            'text': graph.titre,
        },
        'xAxis': {
            'type': 'datetime',
            'plotLines': [{
                'value': 0,
                'width': 1,
                'color': '#808080'
            }],
        },
        'yAxis': {
            'plotLines': [{
                'value': 0,
                'width': 1,
                'color': '#808080'
            }],
        },
    }
    return jsonify(**ans)
