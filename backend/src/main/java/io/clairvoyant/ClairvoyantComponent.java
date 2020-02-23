package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.DashboardApi;
import io.clairvoyant.api.DataPointSocketHandler;
import io.clairvoyant.api.LoginApi;
import io.clairvoyant.api.NodeInfoApi;
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
}
