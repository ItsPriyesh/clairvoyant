package io.clairvoyant;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class ClairvoyantServer {

    private static final int PORT = 8080;

    public static void main(String[] args) throws InterruptedException, IOException {
        // Build DI graph
        ClairvoyantComponent component = DaggerClairvoyantComponent.create();

        component.logger().atInfo().log("Starting server");
        Server server = ServerBuilder
                .forPort(PORT)
                .addService(component.createService())
                .build();

        server.start();

        component.logger().atInfo().log("Listening on port " + PORT);
        server.awaitTermination();

        component.logger().atInfo().log("Server terminated!");
    }
}
