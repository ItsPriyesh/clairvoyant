package io.clairvoyant.api;

import spark.Request;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.util.Arrays;
import java.util.HashSet;

@Singleton
public class ApiService {

    public final LoginApi login;
    public final DashboardApi dash;

    @Inject
    public ApiService(LoginApi login, DashboardApi dash) {
        this.login = login;
        this.dash = dash;
    }

    static boolean hasParams(Request req, String... required) {
        return req.queryParams().containsAll(new HashSet<>(Arrays.asList(required)));
    }
}
