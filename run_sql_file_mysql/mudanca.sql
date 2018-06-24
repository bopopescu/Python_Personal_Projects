set myisam_sort_buffer_size = 1000;
set myisam_repair_threads = 5;

drop table if exists confere.regras;
create table confere.regras(
	a int,
	b int
);
