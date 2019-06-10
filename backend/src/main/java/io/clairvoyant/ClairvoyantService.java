package io.clairvoyant;

import io.clairvoyant.proto.Ack;
import io.clairvoyant.proto.ClairvoyantServiceGrpc;
import io.clairvoyant.proto.DataPoint;
import io.grpc.stub.StreamObserver;

final class ClairvoyantService extends ClairvoyantServiceGrpc.ClairvoyantServiceImplBase {
    @Override
    public void createDataPoint(DataPoint request, StreamObserver<Ack> responseObserver) {
        super.createDataPoint(request, responseObserver);

        // Do stuff with received DataPoint payload

        Ack ack = Ack.newBuilder()
                .setDataPointId(request.getId())
                .build();

        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }
}
