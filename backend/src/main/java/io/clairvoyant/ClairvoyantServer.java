package io.clairvoyant;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class ClairvoyantServer {

    public static void main(String[] args) throws InterruptedException, IOException {
        Server server = ServerBuilder.forPort(8080).addService(new ClairvoyantService()).build();
        server.start();
        server.awaitTermination();
    }
}
