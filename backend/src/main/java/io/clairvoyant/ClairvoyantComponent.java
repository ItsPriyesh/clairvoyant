package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.*;
import io.clairvoyant.gateway.ClairvoyantService;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    LoginApi createLoginApi();
    DashboardApi createDashboardApi();
    NodeInfoApi createNodeInfoApi();
    DataPointSocketHandler createSocketHandler();
    MotionEventSocketHandler createMotionEventSocketHandler();
    HeartbeatSocketHandler createHeartbeatSocketHandler();
}
