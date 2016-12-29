package com.common.insurance.utils;

import android.util.Log;

/**
 * 日志管理器
 */
public class InsuranceLogger {

    public static boolean LOGGER_ON = true;


    public static void d(String tag, String content) {
        if (LOGGER_ON) {
            Log.d(tag, content);
        }
    }
}
