package com.common.insurance.utils;

import java.util.IdentityHashMap;
import java.util.Map;

/**
 * Created by wangyongchao on 16/9/30.
 */
public class InsuranceUtils {

    public static String WeatherUrl = "http://v.juhe.cn/weather/index?cityname=%E5%8C%97%E4%BA%AC&dtype=&format=&key=177038539bb5e9c91c8a1443145d3765";
    public static String WeatherUrlByIp = "http://v.juhe.cn/weather/ip?ip=58.215.185.154&dtype=json&format=&key=177038539bb5e9c91c8a1443145d3765";


    public static Map<String, String> getCommonHeader() {

        IdentityHashMap<String, String> header = new IdentityHashMap<String, String>();

        return header;
    }
}
