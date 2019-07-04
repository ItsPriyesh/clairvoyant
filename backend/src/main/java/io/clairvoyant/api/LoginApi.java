package io.clairvoyant.api;

import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.User;
import io.clairvoyant.model.auto.UserAuto;
import org.davidmoten.rx.jdbc.Database;
import spark.Request;
import spark.Response;

import javax.inject.Inject;

public class LoginApi {

    private final UserStore userStore;

    @Inject
    public LoginApi(UserStore userStore) {
        this.userStore = userStore;
    }

    public String createUser(Request req, Response res) {

        User user = UserAuto.builder()
                // Add fields
                .build();
        userStore.insert(user);

        return "sessiontoken";
    }
}
