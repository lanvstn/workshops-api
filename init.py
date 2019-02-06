#!/usr/bin/env python3

import argparse
import sqlalchemy.exc

from workshops_api.app import app
from workshops_api.database import db
from workshops_api.auth import ACCESS_LEVELS
from workshops_api.models.user import UserModel
from workshops_api.config import config


class Setup():
    def __init__(self, config):
        self.settings = config["init"]

    def run(self):
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Initialized database")

            # Create admin user
            try:
                adminuser = UserModel(
                    id=1,
                    full_name='admin',
                    identity=self.settings["admin_identity"],
                    permission=ACCESS_LEVELS["admin"],
                    event_id=-1
                )
                db.session.add(adminuser)
                db.session.commit()
                print("Created admin")

                # Add test data if needed
                if self.settings["add_testdata"]:
                    from workshops_api.testdata import testdata
                    db.session.add_all(testdata)
                db.session.commit()
                print("Added test data")
            except sqlalchemy.exc.IntegrityError:
                print("Error inserting initial data into database, it already exists. "
                      "Run with --force to delete. Quitting.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force",
                        help="Force initialization, DELETE existing database",
                        action="store_true")
    args = parser.parse_args()

    config.load_config('.')
    setup = Setup(config.config)

    if args.force:
        print("=== WARNING: YOU ARE ABOUT TO DELETE ALL TABLES IN THE DATABASE!!! ===")
        input('    Enter to continue, Ctrl-C to quit > ')

        with app.app_context():
            db.drop_all()
            print("Deleted database.")

    setup.run()
