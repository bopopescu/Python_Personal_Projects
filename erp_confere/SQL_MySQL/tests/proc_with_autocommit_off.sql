-- Test if autocommit works with procedure (it should)
set autocommit = 0;
call prc_insert_pedido_servico(1, 6, null, 0, null, null, '{"status": "novo"}')
