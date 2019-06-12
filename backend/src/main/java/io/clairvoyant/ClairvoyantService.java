package io.clairvoyant;

import io.clairvoyant.proto.Ack;
import io.clairvoyant.proto.ClairvoyantServiceGrpc;
import io.clairvoyant.proto.DataPoint;
import io.grpc.stub.StreamObserver;

final class ClairvoyantService extends ClairvoyantServiceGrpc.ClairvoyantServiceImplBase {
    @Override
    public void createDataPoint(DataPoint request, StreamObserver<Ack> responseObserver) {
        // Do stuff with received DataPoint payload
        System.out.println(request);

        Ack ack = Ack.newBuilder()
                .setDataPointId(request.getId())
                .build();

        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }
}
