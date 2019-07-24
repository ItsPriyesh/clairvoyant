package io.clairvoyant.api;

import com.google.gson.Gson;
import io.clairvoyant.api.model.Error;
import io.clairvoyant.db.UserStore;
import spark.Request;
import spark.Response;

import javax.inject.Inject;
import java.lang.reflect.Type;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Optional;

public abstract class ApiBase {

    private final Gson gson;
    private final UserStore userStore;

    public ApiBase(Gson gson, UserStore userStore) {
        this.gson = gson;
        this.userStore = userStore;
    }

    protected Optional<Error> assertParams(Request req, Response res, String... required) {
        if (req.queryParams().containsAll(new HashSet<>(Arrays.asList(required)))) {
            return Optional.empty();
        } else {
            res.status(400);
            return Optional.of(Error.create("Required parameters not specified!"));
        }
    }

    protected Optional<Error> authenticateUser(Request req, Response res) {
        Optional<Error> err = assertParams(req, res, "user_id", "session_token");
        if (err.isPresent()) {
            res.status(400);
            return err;
        }

        int userId;
        try {
            userId = Integer.parseInt(req.queryParams("user_id"));
        } catch (NumberFormatException e) {
            res.status(400);
            return Optional.of(Error.create(e.getMessage()));
        }

        if (userStore.isUserSessionValid(userId, req.queryParams("session_token")).blockingGet()) {
            return Optional.empty();
        } else {
            res.status(401);
            return Optional.of(Error.create("Invalid credentials!"));
        }
    }

    protected <A> String toJson(A a) {
        return gson.toJson(a);
    }

    protected <A> String toJson(A a, Type type) {
        return gson.toJson(a, type);
    }
}
