NAME="connect_4_game"
DJANGODIR="$(cd "$( dirname "${BASH_SOURCE[0]}")/.." && pwd )"
USER=root
# GROUP=root
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=connect_4_game.settings
DJANGO_WSGI_MODULE=connect_4_game.wsgi

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
        --name $NAME \
        --workers $NUM_WORKERS \
        --max-requests 2000 \
        --user=$USER \
        --bind=0.0.0.0:8006

