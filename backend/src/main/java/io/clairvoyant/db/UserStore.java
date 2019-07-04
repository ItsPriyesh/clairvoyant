package io.clairvoyant.db;

import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;

public class UserStore {

    private final Database database;

    @Inject
    UserStore(Database database) {
        this.database = database;
    }


}
