from bokeh.embed import components 
from bokeh.models import ColumnDataSource 
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from bokeh.plotting import figure

def pedido_loja_bar_char(data):

	source  = ColumnDataSource(data=data)

	plot = 	figure(x_range=data['lojas'], plot_height=400, toolbar_location=None, title="Loja x Pedidos")
	plot.vbar(x='lojas', top='quantidade', width=.9, source=source, legend='lojas', line_color='white', 
			fill_color=factor_cmap('lojas', palette=Spectral6, factors=data['lojas']))

	plot.xgrid.grid_line_color = None

	plot.y_range.start = 0 # Y Start value
	plot.y_range.end = 20 # Y End value

	plot.legend.orientation = 'horizontal'
	plot.legend.location = 'top_center'

	return components(plot)

