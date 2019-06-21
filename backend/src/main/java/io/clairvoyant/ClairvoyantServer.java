package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class ClairvoyantServer {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();
    private static final int PORT = 8080;

    public static void main(String[] args) throws InterruptedException, IOException {
        // Build DI graph
        ClairvoyantComponent component = DaggerClairvoyantComponent.create();

        logger.atInfo().log("Starting server");
        Server server = ServerBuilder
                .forPort(PORT)
                .addService(component.createService())
                .build();

        server.start();

        logger.atInfo().log("Listening on port " + PORT);
        server.awaitTermination();

        logger.atInfo().log("Server terminated!");
    }
}
