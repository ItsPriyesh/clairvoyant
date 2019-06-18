package io.clairvoyant;

import io.clairvoyant.proto.Ack;
import io.clairvoyant.proto.ClairvoyantServiceGrpc;
import io.clairvoyant.proto.DataPoint;
import io.clairvoyant.proto.Heartbeat;
import io.grpc.stub.StreamObserver;

import javax.inject.Inject;

final class ClairvoyantService extends ClairvoyantServiceGrpc.ClairvoyantServiceImplBase {

    private final NodeManager nodeManager;
    private final DataProcessor dataProcessor;

    @Inject
    ClairvoyantService(NodeManager nodeManager, DataProcessor dataProcessor) {
        this.nodeManager = nodeManager;
        this.dataProcessor = dataProcessor;
    }

    @Override
    public void createDataPoint(DataPoint request, StreamObserver<Ack> responseObserver) {
        dataProcessor.processDataPoint(request);

        Ack ack = Ack.newBuilder()
                .setDataPointId(request.getId())
                .build();

        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }

    @Override
    public void ping(Heartbeat heartbeat, StreamObserver<Ack> responseObserver) {
        nodeManager.addNode(heartbeat);

        Ack ack = Ack.newBuilder()
                .setDataPointId(heartbeat.getId())
                .build();

        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }
}
