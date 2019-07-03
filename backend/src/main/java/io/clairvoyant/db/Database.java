package io.clairvoyant.db;

import com.google.auto.value.AutoValue;
import com.mysql.cj.jdbc.MysqlDataSource;
import io.clairvoyant.model.Models;
import io.requery.sql.Configuration;
import io.requery.sql.ConfigurationBuilder;
import io.requery.sql.EntityDataStore;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class Database {

    @AutoValue
    public static abstract class Config {

        public static Builder builder() {
            return new AutoValue_Database_Config.Builder();
        }

        @AutoValue.Builder
        public abstract static class Builder {
            public abstract Builder setAddress(String address);
            public abstract Builder setPort(int port);
            public abstract Builder setUser(String user);
            public abstract Builder setPassword(String password);

            public abstract Config build();
        }

        public abstract String address();
        public abstract int port();
        public abstract String user();
        public abstract String password();
    }

    private final EntityDataStore dataStore;

    @Inject
    public Database(Config dbConfig) {
        MysqlDataSource source = new MysqlDataSource();
        source.setServerName(dbConfig.address());
        source.setPort(dbConfig.port());
        source.setUser(dbConfig.user());
        source.setPassword(dbConfig.password());

        Configuration config = new ConfigurationBuilder(source, Models.DEFAULT).build();
        dataStore = new EntityDataStore<>(config);
    }

    public EntityDataStore get() {
        return dataStore;
    }
}
