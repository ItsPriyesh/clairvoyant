package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.api.DashboardApi;
import io.clairvoyant.api.LoginApi;
import io.clairvoyant.api.NodeInfoApi;
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

        setupApi(component, frontendPort);

        server.awaitTermination();
        logger.atInfo().log("Server terminated!");
    }

    private static void setupApi(ClairvoyantComponent component, int port) {
        logger.atInfo().log("Starting web API");
        Spark.port(port);
        logger.atInfo().log("Listening for frontend on port " + port);

        Spark.webSocket("/listenDataPoint", component.createSocketHandler());

        Spark.before((req, res) -> {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Content-Type", "application/json");
            res.header("X-Content-Type-Options", "nosniff");
        });

        LoginApi login = component.createLoginApi();
        Spark.post("/createUser", login::createUser);
        Spark.get("/login", login::login);

        DashboardApi dash = component.createDashboardApi();
        Spark.get("/datapoints", dash::getDataPoints);
        Spark.get("/nodes", dash::getNodes);

        NodeInfoApi nodeInfo = component.createNodeInfoApi();
        Spark.get("/nodeInfo", nodeInfo::getDataPointsForNode);

        Spark.get("/motionevents", dash::getMotionEvents);
    }
}
