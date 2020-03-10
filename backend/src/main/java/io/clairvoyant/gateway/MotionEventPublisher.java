package io.clairvoyant.gateway;

import io.clairvoyant.db.UserStore;
import io.clairvoyant.proto.DataPoint;
import io.clairvoyant.proto.MotionEvent;
import io.reactivex.Observable;
import io.reactivex.subjects.PublishSubject;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class MotionEventPublisher {

    private final UserStore userStore;
    private final PublishSubject<MotionEvent> subject = PublishSubject.create();

    @Inject
    MotionEventPublisher(UserStore userStore) {
        this.userStore = userStore;
    }

    public void publish(MotionEvent motionEvent) {
        subject.onNext(motionEvent);
    }

    public Observable<MotionEvent> listenForUser(int userId) {
        return subject
                .flatMapSingle(motionEvent -> userStore
                        .getUserForNode(motionEvent.getNodeId())
                        .map(u -> new MotionEventUser(motionEvent, u))
                )
                .filter(d -> d.userId == userId)
                .map(d -> d.motionEvent);
    }

    private static class MotionEventUser {
        private final MotionEvent motionEvent;
        private final int userId;

        MotionEventUser(MotionEvent motionEvent, int userId) {
            this.motionEvent = motionEvent;
            this.userId = userId;
        }
    }
}
