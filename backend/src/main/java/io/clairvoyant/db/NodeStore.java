package io.clairvoyant.db;

import io.clairvoyant.model.Node;
import io.clairvoyant.proto.DataPoint;
import io.reactivex.Completable;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;

public class NodeStore {

    private final Database database;

    @Inject
    UserStore(Database database) {
        this.database = database;
    }

    public Completable insert(Node node) {
        return database
                .update("insert into DataPoint values(?, ?, FROM_UNIXTIME(?), ?, ?)")
                .parameters(
                        point.getId(),
                        point.getNodeId(),
                        point.getTimestamp(),
                        point.getEventType(),
                        point.getConfidence()
                )
                .complete();
    }
}
