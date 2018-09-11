from flask import Blueprint, render_template, url_for, request, redirect, jsonify
from services import servico_service

bp = Blueprint('pedido_servico', __name__, '/pedido_servico')

@bp.route('<int:pedido>/pedido_servico')
