package io.clairvoyant;

import dagger.Component;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createService();
}
