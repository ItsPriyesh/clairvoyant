package io.clairvoyant.api;

import io.clairvoyant.proto.DataPoint;
import io.reactivex.Observable;
import io.reactivex.subjects.PublishSubject;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class DataPointPublisher {

    private final PublishSubject<DataPoint> subject = PublishSubject.create();

    @Inject
    DataPointPublisher() {}

    public void publish(DataPoint dataPoint) {
        subject.onNext(dataPoint);
    }

    public Observable<DataPoint> listen(int userID) {
        return subject;
    }
}
