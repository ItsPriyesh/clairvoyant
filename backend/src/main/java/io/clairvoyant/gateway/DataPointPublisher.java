package io.clairvoyant.gateway;

import io.clairvoyant.db.UserStore;
import io.clairvoyant.proto.DataPoint;
import io.reactivex.Observable;
import io.reactivex.subjects.PublishSubject;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class DataPointPublisher {

    private final UserStore userStore;
    private final PublishSubject<DataPoint> subject = PublishSubject.create();

    @Inject
    DataPointPublisher(UserStore userStore) {
        this.userStore = userStore;
    }

    public void publish(DataPoint dataPoint) {
        subject.onNext(dataPoint);
    }

    public Observable<DataPoint> listenForUser(int userId) {
        return subject
                .flatMapSingle(dataPoint -> userStore
                        .getUserForNode(dataPoint.getNodeId())
                        .map(u -> new DataPointUser(dataPoint, u))
                )
                .filter(d -> d.userId == userId)
                .map(d -> d.dataPoint);
    }

    private static class DataPointUser {
        private final DataPoint dataPoint;
        private final int userId;

        DataPointUser(DataPoint dataPoint, int userId) {
            this.dataPoint = dataPoint;
            this.userId = userId;
        }
    }
}
