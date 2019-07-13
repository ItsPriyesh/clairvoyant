package io.clairvoyant.db;

import io.clairvoyant.proto.DataPoint;
import io.reactivex.Completable;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;

public class DataPointStore {

    private final Database database;

    @Inject
    public DataPointStore(Database database) {
        this.database = database;
    }

    public Completable insert(DataPoint point) {
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

    // overload to support test data service
    public Completable insert(io.clairvoyant.model.DataPoint point) {
        return database
                .update("insert into DataPoint values(?, ?, FROM_UNIXTIME(?), ?, ?)")
                .parameters(
                        point.dataPointID(),
                        point.nodeID(),
                        point.receivedAt(),
                        point.eventType(),
                        point.confidence()
                )
                .complete();
    }
}
