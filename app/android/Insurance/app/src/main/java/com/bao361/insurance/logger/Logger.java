package com.bao361.insurance.logger;

import android.util.Log;

/**
 * @author：wangyongchao on 17/5/13 15:38
 */
public class Logger {

    public static boolean isEnable = false;


    public static void v(String tag, String msg) {
        if (isEnable) {
            Log.v(tag, msg);
        }

    }

    public static void v(String tag, String msg, Throwable tr) {
        if (isEnable) {
            Log.v(tag, msg, tr);
        }
    }

    public static void d(String tag, String msg) {
        if (isEnable) {
            Log.d(tag, msg);
        }
    }

    public static void d(String tag, String msg, Throwable tr) {
        if (isEnable) {
            Log.d(tag, msg, tr);
        }
    }

    public static void i(String tag, String msg) {
        if (isEnable) {
            Log.i(tag, msg);
        }
    }

    public static void i(String tag, String msg, Throwable tr) {
        if (isEnable) {
            Log.i(tag, msg, tr);
        }
    }

    public static void w(String tag, String msg) {
        if (isEnable) {
            Log.w(tag, msg);
        }
    }

    public static void w(String tag, String msg, Throwable tr) {
        if (isEnable) {
            Log.w(tag, msg, tr);
        }
    }

    public static void w(String tag, Throwable tr) {
        if (isEnable) {
            Log.w(tag, tr);
        }
    }

    public static void e(String tag, String msg) {
        if (isEnable) {
            Log.e(tag, msg);
        }
    }

    public static void e(String tag, String msg, Throwable tr) {
        if (isEnable) {
            Log.e(tag, msg, tr);
        }
    }


}
