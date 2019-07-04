package io.clairvoyant.api;

import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.User;
import io.clairvoyant.model.auto.UserAuto;
import spark.Request;
import spark.Response;

import javax.inject.Inject;
import java.sql.Date;
import java.util.Arrays;
import java.util.HashSet;
import java.util.UUID;

public class LoginApi {

    private final UserStore userStore;
    private final PasswordManager passManager;

    @Inject
    public LoginApi(UserStore userStore, PasswordManager passManager) {
        this.userStore = userStore;
        this.passManager = passManager;
    }

    public String createUser(Request req, Response res) {
        if (!hasParams(req, "firstName", "lastName", "email", "password")) {
            res.status(400);
            return "Required parameters not specified!";
        }

        String sessionToken = UUID.randomUUID().toString();

        User user = UserAuto.builder()
                .setFirstName(req.queryParams("firstName"))
                .setLastName(req.queryParams("lastName"))
                .setEmail(req.queryParams("email"))
                .setPasswordHash(passManager.hash(req.queryParams("password")))
                .setCreatedAt(new Date(System.currentTimeMillis()))
                .setSessionToken(sessionToken)
                .build();

        System.out.println(user);
        Throwable error = userStore.insert(user).blockingGet();
        if (error == null) {
            res.status(200);
            return sessionToken;
        } else {
            res.status(500);
            return error.getMessage();
        }
    }

    public String login(Request req, Response res) {
        // params could be (username + pass) or sessionToken
        return null;
    }

    private static boolean hasParams(Request req, String... required) {
        return req.queryParams().containsAll(new HashSet<>(Arrays.asList(required)));
    }
}
