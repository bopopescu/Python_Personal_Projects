from bokeh.embed import components 
from bokeh.models import ColumnDataSource 
from bokeh.palettes import Spectral6, Category20c
from bokeh.transform import factor_cmap, cumsum
from bokeh.plotting import figure
from collections import Counter
from math import pi

import pandas as pd

def pedido_loja_bar_char(data):

	title = "Loja x Pedidos: %s - %s" % (data.pop('data_inicio').strftime('%d/%m/%Y'), data.pop('data_fim').strftime('%d/%m/%Y'))
	source  = ColumnDataSource(data=data)

	plot = 	figure(x_range=data['lojas'], plot_height=200, plot_width=400, toolbar_location=None, 
			title= title)
	plot.vbar(x='lojas', top='quantidade', width=.3, source=source, legend='lojas', line_color='white', 
			fill_color=factor_cmap('lojas', palette=Spectral6, factors=data['lojas']))

	plot.xgrid.grid_line_color = None

	plot.y_range.start = 0 # Y Start value
	plot.y_range.end = 15 # Y End value

	plot.legend.orientation = 'horizontal'
	plot.legend.location = 'top_center'

	return components(plot)


def funcionario_pedido_mes_pie_chart(dictionary):

	title = "Pie Chart: {} - {}".format(dictionary.pop('data_inicio').strftime('%d/%m%Y'), dictionary.pop('data_fim').strftime('%d/%m%Y'))
	
	x = Counter(dictionary)
	# colors_count = len(x)

	data = pd.DataFrame.from_dict(dict(x), orient='index')\
						.reset_index()\
						.rename(index=str, columns={0: 'value', 'index': 'Funcionários'})

	data['angle'] = data['value'] / sum(x.values()) * 2*pi
	data['color'] = Category20c(1)

	p = figure(plot_height=350, title=title, toolbar_location=None, tools='hover', tooltips="@country: @value")

	p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), 
		line_color="white", fill_color='color', legend='country', source=data)

	p.axis.axis_label = None
	p.axis.visible = False
	p.grid.grid_line_color = None

	return components(p)