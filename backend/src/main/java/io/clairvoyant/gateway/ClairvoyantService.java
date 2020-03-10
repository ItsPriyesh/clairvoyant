package io.clairvoyant.gateway;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.db.MotionEventStore;
import io.clairvoyant.db.NodeStore;
import io.clairvoyant.proto.*;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import io.reactivex.Completable;
import io.reactivex.schedulers.Schedulers;

import javax.inject.Inject;

public final class ClairvoyantService extends ClairvoyantServiceGrpc.ClairvoyantServiceImplBase {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    private final DataPointStore dataPointStore;
    private final DataPointPublisher dataPointPublisher;
    private final MotionEventPublisher motionEventPublisher;
    private final NodeStore nodeStore;
    private final MotionEventStore motionEventStore;

    @Inject
    ClairvoyantService(DataPointStore dataPointStore, DataPointPublisher dataPointPublisher,
                       MotionEventPublisher motionEventPublisher, NodeStore nodeStore, MotionEventStore motionEventStore) {
        this.dataPointStore = dataPointStore;
        this.dataPointPublisher = dataPointPublisher;
        this.motionEventPublisher = motionEventPublisher;
        this.nodeStore = nodeStore;
        this.motionEventStore = motionEventStore;
    }

    @Override
    public void createDataPoint(DataPoint dataPoint, StreamObserver<Ack> response) {
        dataPointStore
                .contains(dataPoint)
                .flatMapCompletable(exists -> {
                    if (!exists) {
                        return dataPointStore
                                .insert(dataPoint)
                                .doOnComplete(() -> dataPointPublisher.publish(dataPoint));
                    } else {
                        // Return an ack if we already have the datapoint
                        return Completable.complete();
                    }
                })
                .subscribeOn(Schedulers.newThread())
                .subscribe(() -> {
                    Ack ack = Ack.newBuilder()
                            .setMessageId(dataPoint.getMessageId())
                            .setNodeId(dataPoint.getNodeId())
                            .build();

                    logger.atInfo().log("DataPoint %s created", dataPoint.getMessageId());

                    response.onNext(ack);
                    response.onCompleted();
                }, error -> {
                    error.printStackTrace();
                    logger.atInfo().log("Failed to insert DataPoint", error);
                    response.onError(Status.fromThrowable(error).asException());
                });
    }

    @Override
    public void ping(Heartbeat heartbeat, StreamObserver<Ack> responseObserver) {
        nodeStore
                .insert(heartbeat)
                .subscribe(() -> {
                    Ack ack = Ack.newBuilder()
                            .setMessageId(heartbeat.getMessageId())
                            .setNodeId(heartbeat.getNodeId())
                            .build();

                    logger.atInfo()
                            .log("Heartbeat created for Node %s", heartbeat.getNodeId());

                    responseObserver.onNext(ack);
                    responseObserver.onCompleted();
                }, error -> {
                    error.printStackTrace();
                    logger.atInfo().log("Failed to insert Heartbeat", error);
                    responseObserver.onError(Status.fromThrowable(error).asException());
                });
    }

    @Override
    public void createMotionEvent(MotionEvent request, StreamObserver<Ack> response) {
        motionEventStore
                .contains(request)
                .flatMapCompletable(exists -> {
                    if (!exists) {
                        return motionEventStore
                                .insert(request)
                                .doOnComplete(() -> motionEventPublisher.publish(request));
                    } else {
                        // Return an ack if we already have the datapoint
                        return Completable.complete();
                    }
                })
                .subscribeOn(Schedulers.newThread())
                .subscribe(() -> {
                    Ack ack = Ack.newBuilder()
                            .setMessageId(request.getMessageId())
                            .setNodeId(request.getNodeId())
                            .build();

                    logger.atInfo().log("MotionEvent %s created", request.getMessageId());

                    response.onNext(ack);
                    response.onCompleted();
                }, error -> {
                    error.printStackTrace();
                    logger.atInfo().log("Failed to insert MotionEvent", error);
                    response.onError(Status.fromThrowable(error).asException());
                });
    }
}
