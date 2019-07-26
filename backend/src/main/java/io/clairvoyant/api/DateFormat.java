package io.clairvoyant.api;

import java.sql.Date;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Locale;

public class DateFormat {
    public static String toReadableDate(Timestamp timestamp) {
        return new SimpleDateFormat("MMM, dd, yyyy h:mm:ss a ", Locale.US)
                .format(Date.from(timestamp.toInstant()));
    }
}
