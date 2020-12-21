from config import Config
from oasystem import createApp, db
from flask_migrate import MigrateCommand
from flask_script import Command
from flask_script import Manager

app = createApp(Config)


class SayHello(Command):

    def run(self):
        print('say hello...')


class RunServer(Command):

    def run(self):
        db.create_all(app=app)
        app.run(debug=True, port=8000)


manager = Manager(app)
manager.add_command('sayhello', SayHello)
manager.add_command('run', RunServer)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
