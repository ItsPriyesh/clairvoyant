package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.proto.DataPoint;

import javax.inject.Inject;

public class DataProcessor {

    private final FluentLogger logger;

    @Inject DataProcessor(FluentLogger logger) {
        this.logger = logger;
    }

    void processDataPoint(DataPoint dataPoint) {
        logger.atInfo().log("Received datapoint %s", dataPoint.getId());
        switch (dataPoint.getPayloadTypeCase()) {
            case VOICE_PAYLOAD:
                break;
            case VEHICLE_PAYLOAD:
                break;
            case MISSILE_PAYLOAD:
                break;
            case GUNSHOT_PAYLOAD:
                break;
        }
    }
}
