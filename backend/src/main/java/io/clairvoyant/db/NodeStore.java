package io.clairvoyant.db;

import io.clairvoyant.proto.Heartbeat;
import io.reactivex.Completable;
import io.reactivex.Single;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;
import java.util.List;

public class NodeStore {

    private final Database database;
    private final UserStore userStore;

    @Inject
    public NodeStore(Database database, UserStore userStore) {
        this.database = database;
        this.userStore = userStore;
    }

    public Single<List<String>> getNodes(int userId) {
        return database
                .select("select distinct node_id from Node where user_id = ?")
                .parameter(userId)
                .getAs(String.class)
                .toList();
    }

    public Completable insert(Heartbeat node) {
        int userId = userStore
                .getUserForNode(node.getNodeId()).blockingGet();

        return database
                .update("insert into Node values(?, from_unixtime(?), ?, ?)")
                .parameters(
                      node.getNodeId(),
                      node.getTimestamp(),
                      userId,
                      node.getBatteryLevel()
                )
                .complete();
    }
}