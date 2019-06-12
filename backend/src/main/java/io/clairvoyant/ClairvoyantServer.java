package io.clairvoyant;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class ClairvoyantServer {

    private static final int PORT = 8080;

    public static void main(String[] args) throws InterruptedException, IOException {
        Server server = ServerBuilder.forPort(PORT).addService(new ClairvoyantService()).build();
        server.start();
        System.out.println("Running server on port " + PORT);
        server.awaitTermination();
    }
}
