package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.api.ApiService;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import spark.Spark;

import java.io.IOException;

public class ClairvoyantServer {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    /**
     * Usage:
     * java ClairvoyantServer <gateway_port> <web_api_port> <test_mode>
     */
    public static void main(String[] args) throws InterruptedException, IOException {
        if (args.length != 3) {
            throw new IllegalArgumentException(
                    "Ports for gateway service and web API must be specified!");
        }

        final int gatewayPort = Integer.parseInt(args[0]);
        final int frontendPort = Integer.parseInt(args[1]);
        final boolean testMode = Boolean.parseBoolean(args[2]);

        // Build DI graph
        ClairvoyantComponent component = DaggerClairvoyantComponent.create();

        logger.atInfo().log("Starting gRPC server");
        Server server = ServerBuilder
                .forPort(gatewayPort)
                .addService(component.createGatewayRpcService())
                .build();

        server.start();
        logger.atInfo().log("Listening for gateway on port " + gatewayPort);

        logger.atInfo().log("Starting web API");
        ApiService api = component.createWebApiService();
        Spark.port(frontendPort);
        logger.atInfo().log("Listening for frontend on port " + frontendPort);

        Spark.post("/createUser", api.login::createUser);
        Spark.get("/login", api.login::login);

        if(testMode) {
            // create test data
            try {
                logger.atInfo().log("Creating test user...");
                component.createTestUser().createUser();
                logger.atInfo().log("User created");

                logger.atInfo().log("Creating test datapoints...");
                component.createTestDataPoint().createDataPoint();
                logger.atInfo().log("Datapoints created");
            } catch(Exception ex) {
                // do smthg
            }
        }

        server.awaitTermination();
        logger.atInfo().log("Server terminated!");
    }
}
