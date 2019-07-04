package io.clairvoyant.api;

import org.davidmoten.rx.jdbc.Database;
import spark.Request;
import spark.Response;

import javax.inject.Inject;

public class WebApiService {

    private final Database database;

    @Inject
    public WebApiService(Database database) {
        this.database = database;
    }

    public String createUser(Request req, Response res) {
        return "hi";
    }
}
