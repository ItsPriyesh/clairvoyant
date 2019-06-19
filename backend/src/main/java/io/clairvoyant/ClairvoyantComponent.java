package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import dagger.Component;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    FluentLogger logger();
    ClairvoyantService createService();
}
