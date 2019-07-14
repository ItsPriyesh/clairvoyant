package io.clairvoyant.api;

import com.google.gson.Gson;
import io.clairvoyant.api.model.Error;
import io.clairvoyant.api.model.SessionToken;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.User;
import io.clairvoyant.model.auto.UserAuto;
import io.reactivex.Maybe;
import spark.Request;
import spark.Response;

import javax.inject.Inject;
import java.sql.Timestamp;
import java.util.Optional;
import java.util.UUID;

public class LoginApi extends ApiBase {

    private final UserStore userStore;
    private final PasswordManager passManager;

    @Inject
    public LoginApi(UserStore userStore, PasswordManager passManager, Gson gson) {
        super(gson, userStore);
        this.userStore = userStore;
        this.passManager = passManager;
    }

    public String createUser(Request req, Response res) {
        Optional<Error> err = assertParams(req, res, "firstName", "lastName", "email", "password");
        if (err.isPresent()) return toJson(err.get());

        String sessionToken = UUID.randomUUID().toString();

        User user = UserAuto.builder()
                .setFirstName(req.queryParams("firstName"))
                .setLastName(req.queryParams("lastName"))
                .setEmail(req.queryParams("email"))
                .setPasswordHash(passManager.hash(req.queryParams("password")))
                .setCreatedAt(new Timestamp(System.currentTimeMillis()))
                .setSessionToken(sessionToken)
                .build();

        Throwable insertErr = userStore.insert(user).blockingGet();
        if (insertErr == null) {
            res.status(200);
            return toJson(SessionToken.create(sessionToken));
        } else {
            res.status(500);
            return toJson(Error.create(insertErr.getMessage()));
        }
    }

    public String login(Request req, Response res) {
        Optional<Error> error = assertParams(req, res, "email", "password");
        if (error.isPresent()) return toJson(error);

        Maybe<User> userMaybe = userStore.getUser(req.queryParams("email"));
        if (userMaybe.isEmpty().blockingGet()) {
            res.status(400);
            return toJson(Error.create("Invalid email!"));
        }

        User user = userMaybe.blockingGet();
        if (passManager.check(req.queryParams("password"), user.passwordHash())) {
            res.status(200);
            return toJson(SessionToken.create(user.sessionToken()));
        } else {
            res.status(400);
            return toJson(Error.create("Invalid password!"));
        }
    }
}
