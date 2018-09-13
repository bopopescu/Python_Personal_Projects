jQuery(document).ready(function($) {

	$('.datepicker').datepicker({dateFormat: 'dd/mm/yy'})
	console.log('Entrou/?')
	$('#cep').focusout(function(){
		if ($(this).val() != '' && $(this).val() == 8){
			$.get('https://viacep.com.br/ws/' + $(this).val() + '/json/', function(data, status, xhr) {
				if(status == "success"){
					if(!data.erro){
						$('#endereco').val(data.logradouro + ' ' + data.complemento)
						$('#bairro').val(data.bairro)
						$('#cidade').val(data.localidade)
						$('#uf').val(data.uf)
						/*$('#cep').addClass('is-valid')
						$('#cep').removeClass('is-invalid')*/
					} else {
						/*$('#cep').addClass('is-invalid')
						$('#cep').removeClass('is-valid')*/
					}
				}
			});	
		} else {
			console.log('Errrrrou')
		}
	});

	$('input[type="text"]').focusout(function(event) {
		$(this).val($(this).val().trim())
	});

	$('.ambiente-selected').attr('name', $('.ambiente-selected').children('option:selected').text().trim().replace(' ', '-').toLowerCase());
	$('.ambiente-selected').parent().siblings('div').children('div').children('input')
	.attr('name', 'quantidade-'+ $('.ambiente-selected').children('option:selected').text().trim().replace(' ', '-').toLowerCase())

	function reloadProps(){
		$('.numeric').numeric({negative: false});
		$('.real-value').numeric({decimalPlaces:2, altDecimal: '.', decimal:',', negative: false})		
	}

	$('#pedido-cadastrar').on('click', '.minus-quantidade-form', function(event) {
		event.preventDefault()
		
		$(this).parent().parent().parent().parent().remove()
	});

	// New ambiente select 
	$("#pedido-cadastrar").on("click", '.add-quantidade-form', function(event) { 
		console.log('entrou')
		event.preventDefault()

		currentAmbientes = ambientes.filter(function(element) {
			var nomeElement = element.nome.trim().split(' ').join('-').toLowerCase()
			
			return !$('select[name='+nomeElement).length
		})

		if(currentAmbientes.length > 0){

			var selectedAmbiente = $('select[name="select-ambientes[]"]').val()
			console.log(selectedAmbiente)

			var selectAmbiente = $('<select></select>', {
				class: 'form-control ambiente-selected', 
				form: 'pedido-cadastrar', 
				name: currentAmbientes[0]['nome'].trim().split(' ').join('-').toLowerCase()
			})
			
			currentAmbientes.map(function(element) {		
				selectAmbiente.append($('<option></option>', {
					value: element['codigo'],
					text: element['nome']
				}))	
				
			})

			nomeAmbiente = currentAmbientes[0]['nome'].trim().split(' ').join('-').toLowerCase()

			/*
				Para cada ambiente selecionado, criar um campo novo para entrar o ambiente
			*/
			var rootDiv = $('<div></div>', {class: 'form-row select-ambiente'})
			var firstChildDiv = $('<div></div>', {class: 'form-group col-sm-3'})
			var secondChildDiv = $('<div></div>', {class: 'form-group col-sm-2'})
			var secondChildInnerDiv = $('<div></div>', {class: 'input-group', name: 'ambiente'})
			var inputQuantidade = $('<input/>', {class: 'form-control col-sm-4 numeric', 
				type: 'text', name: 'quantidade-'+ nomeAmbiente, required: true})
			var spanAddBtn = $('<span></span>', {class: 'input-group-btn'})
			var btnAdd = $('<button></button>', {class: 'btn btn-default add-quantidade-form', text: '+'})
			var spanSbtBtn = $('<span></span>', {class: 'input-group-btn'})
			var btnSbt = $('<button></button>', {class: 'btn btn-default minus-quantidade-form', text: '-'})

			rootDiv.append(firstChildDiv)
			rootDiv.append(secondChildDiv)

			firstChildDiv.append(selectAmbiente)
			secondChildDiv.append(secondChildInnerDiv)

			secondChildInnerDiv.append(inputQuantidade)
			secondChildInnerDiv.append(spanAddBtn)
			secondChildInnerDiv.append(spanSbtBtn)

			spanSbtBtn.append(btnSbt)
			spanAddBtn.append(btnAdd)

			rootDiv.insertBefore('.submit-form')

			reloadProps()
		}
	})

	$('#pedido-cadastrar').on('change', '.ambiente-selected', function(event) {
		event.preventDefault();
		/* Act on the event */
		var attributeName = $(this).children('option:selected').text().trim().split(' ').join('-').toLowerCase();

		$(this).attr('name', attributeName)
		$(this).parent().siblings('div').children('div').children('input')
		.attr('name', 'quantidade-'+ attributeName)

	});

	$('.numeric').numeric({negative: false});
	$('.real-value').numeric({decimalPlaces:2, altDecimal: '.', decimal:',', negative: false});

});