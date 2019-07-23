package io.clairvoyant.db;

import io.reactivex.Single;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;
import java.util.List;

public class NodeStore {

    private final Database database;

    @Inject
    public NodeStore(Database database) {
        this.database = database;
    }

    public Single<List<String>> getNodes(int userId) {
        return database
                .select("select distinct node_id from Node where user_id = ?")
                .parameter(userId)
                .getAs(String.class)
                .toList();
    }
}