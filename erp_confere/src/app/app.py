import services.cliente_service as cliente_service
import services.cliente_endereco_service as cliente_endereco
import services.pedido_service as pedido_service

pedido = {
	"numero": "HJN4",
	"valor": 100000.99,
	"data_entrada": "2018-07-10",
	"data_inicio": "2018-07-19",
	"data_fim": "2018-07-30",
	"ambiente": [
		{
			"nome": "quarto",
			"quantidade": 10
		},
		{
			"nome": "banheiro",
			"quantidade": 2
		},
		{
			"nome": "sala",
			"quantidade": 3
		}
	],
	"endereco": {
		"cep": "01526000",
		"rua": "Rua Bueno de Andrade",
		"numero": 769,
		"bairro": "Aclimação",
		"cidade": "São Paulo",
		"complemento": "apto 44 / Bloco 2"
	},
	"loja": {
		"codigo": 1
	},
	"cliente": {
		"nome": "Vinicius",
		"sobrenome": "Akiyama Hashizumi Yosiura",
		"email": "viniahy@gmail.com",
		"telefone_celular": 979863277
	},
	"servicos": [
		{"codigo": 1},
		{"codigo": 2},
		{"codigo": 3},
		{"codigo": 4},
		{"codigo": 5}
	]
}


pedido_service.insert_pedido(pedido)