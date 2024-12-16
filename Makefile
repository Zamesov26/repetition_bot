ALEMBIC_CONFIG=app/store/pg/alembic.ini

revision:
	alembic --config $(ALEMBIC_CONFIG) revision --autogenerate -m "temp"

upgrade:
	alembic --config $(ALEMBIC_CONFIG) upgrade head