package io.clairvoyant.db;

import io.clairvoyant.model.User;
import io.reactivex.Completable;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;

public class UserStore {

    private final Database database;

    @Inject
    UserStore(Database database) {
        this.database = database;
    }

    public Completable insert(User user) {
        return database
                .update("insert into User values(?, ?, ?, ?, ?, ?")
                .parameters(
                        null,
                        user.firstName(),
                        user.lastName(),
                        user.email(),
                        user.createdAt(),
                        user.passwordHash()
                )
                .complete();
    }
}
