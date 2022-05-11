from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Pitch

# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server', Server)

# initialize our Migrate class
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
@manager.shell
def make_shell_context():
    return dict(db=db,pitch=Pitch)

if __name__ == '__main__':
    app.run()