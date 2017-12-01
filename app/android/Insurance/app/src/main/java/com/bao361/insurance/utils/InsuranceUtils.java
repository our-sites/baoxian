package com.bao361.insurance.utils;

import android.content.Context;

import java.util.IdentityHashMap;
import java.util.Map;

/**
 * Created by wangyongchao on 16/9/30.
 */
public class InsuranceUtils {

    public static Map<String, String> getCommonHeader() {

        IdentityHashMap<String, String> header = new IdentityHashMap<String, String>();

        return header;
    }

    /**
     * 根据手机的分辨率从 dp 的单位 转成为 px(像素)
     */
    public static int dip2px(Context context, float dpValue) {
        final float scale = context.getResources().getDisplayMetrics().density;
        return (int) (dpValue * scale + 0.5f);
    }

    /**
     * 根据手机的分辨率从 px(像素) 的单位 转成为 dp
     */
    public static int px2dip(Context context, float pxValue) {
        final float scale = context.getResources().getDisplayMetrics().density;
        return (int) (pxValue / scale + 0.5f);
    }
}
