package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.api.LoginApi;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import spark.Spark;

import java.io.IOException;

public class ClairvoyantServer {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    /**
     * Usage:
     * java ClairvoyantServer <gateway_port> <web_api_port>
     */
    public static void main(String[] args) throws InterruptedException, IOException {
        if (args.length != 2) {
            throw new IllegalArgumentException(
                    "Ports for gateway service and web API must be specified!");
        }

        final int gatewayPort = Integer.parseInt(args[0]);
        final int frontendPort = Integer.parseInt(args[1]);

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
        LoginApi api = component.createWebApiService();
        Spark.port(frontendPort);
        logger.atInfo().log("Listening for frontend on port " + frontendPort);

        Spark.get("/createUser", api::createUser);

        server.awaitTermination();
        logger.atInfo().log("Server terminated!");
    }
}
