CREATE TABLE operation_logs(
	id bigserial,
	data json,
	token text primary key
);