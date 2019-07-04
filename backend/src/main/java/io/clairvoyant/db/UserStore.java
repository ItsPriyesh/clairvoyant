package io.clairvoyant.db;

import io.clairvoyant.model.User;
import io.reactivex.Completable;
import io.reactivex.Maybe;
import io.reactivex.Single;
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
                .update("insert into User values(?, ?, ?, ?, ?, ?, ?)")
                .parameters(
                        null,
                        user.firstName(),
                        user.lastName(),
                        user.email(),
                        user.createdAt(),
                        user.passwordHash(),
                        user.sessionToken()
                )
                .complete();
    }

    public Maybe<String> getSessionToken(String userEmail) {
        return database.select("select * from User where email = ?")
                .parameter(userEmail)
                .autoMap(User.class)
                .toList()
                .flatMapMaybe(users -> users.isEmpty()
                        ? Maybe.empty()
                        : Maybe.just(users.get(0).sessionToken())
                );
    }
}
