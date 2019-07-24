package io.clairvoyant.gateway;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.proto.Ack;
import io.clairvoyant.proto.ClairvoyantServiceGrpc;
import io.clairvoyant.proto.DataPoint;
import io.clairvoyant.proto.Heartbeat;
import io.grpc.stub.StreamObserver;

import javax.inject.Inject;

public final class ClairvoyantService extends ClairvoyantServiceGrpc.ClairvoyantServiceImplBase {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    private final DataPointStore dataPointStore;
    private final DataPointPublisher dataPointPublisher;

    @Inject
    ClairvoyantService(DataPointStore dataPointStore, DataPointPublisher dataPointPublisher) {
        this.dataPointStore = dataPointStore;
        this.dataPointPublisher = dataPointPublisher;
    }

    @Override
    public void createDataPoint(DataPoint dataPoint, StreamObserver<Ack> response) {
      logger.atInfo().log(String.format("Receiving datapoint %s", dataPoint.toString()));
      Ack ack = Ack.newBuilder()
        .setMessageId(dataPoint.getMessageId())
        .setNodeId(dataPoint.getNodeId())
        .build();
      logger.atInfo().log(ack.toString());

      response.onNext(ack);
      response.onCompleted();
//        dataPointStore
//                .insert(dataPoint)
//                .doOnComplete(() -> dataPointPublisher.publish(dataPoint))
//                .subscribe(() -> {
//                    Ack ack = Ack.newBuilder()
//                            .setMessageId(dataPoint.getMessageId())
//                            .setNodeId(dataPoint.getNodeId())
//                            .build();
//                    logger.atInfo()
//                        .log("DataPoint %s created", dataPoint.getMessageId());
//                    response.onNext(ack);
//                    response.onCompleted();
//                }, error -> {
//                    error.printStackTrace();
//                    logger.atInfo().log("Failed to insert DataPoint", error);
//                    response.onError(error);
//                });
    }

    @Override
    public void ping(Heartbeat heartbeat, StreamObserver<Ack> responseObserver) {
        logger.atInfo().log(String.format("Receiving heartbeat %s", heartbeat.toString()));
        Ack ack = Ack.newBuilder()
                .setMessageId(heartbeat.getMessageId())
                .setNodeId(heartbeat.getNodeId())
                .build();
        logger.atInfo().log(ack.toString());

        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }
}
