package io.clairvoyant.db;

import io.clairvoyant.proto.DataPoint;
import io.reactivex.Completable;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;

public class DataPointStore {

    private final Database db;

    @Inject
    public DataPointStore(Database database) {
        db = database;
    }

    public Completable insert(DataPoint point) {
        return db
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
