import  services.cliente_service as cliente_service


cliente = {
		"nome": "Vinicius",
		"sobrenome": "Akiyama Hashizumi Yosiura",
		"email": "viniahy@gmail.com",
		"telefone_celular": 979863277
}


cliente_service.verify_cliente(cliente)