package com.bao361.insurance.utils;

import android.text.TextUtils;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Json相关处理
 */
public class JsonUtil {


    private JsonUtil() {
    }

    /**
     * 将Map转化为JsonObj格式的字符串
     *
     * @param params 注意参数若为{@link IdentityHashMap}
     *               ，则Map中可能包含同名的键，则对于多于一个元素的key，则转化为JsonArray
     * @return
     */
    public static JSONObject parseMap2JsonObject(Map<String, String> params) {
        JSONObject jsonObj = parseMap2Json(transMap(params));
        return jsonObj;
    }

    /**
     * 将Map转化为JsonObj对象，如果某一个字段需要JsonArray类型，请传参的时候把其转化为JsonArray形式的字符串
     *
     * @param values 如果键值的条目大于1，则转化为JsonArray
     * @return
     */
    private static JSONObject parseMap2Json(
            Map<String, ArrayList<String>> values) {

        JSONObject resultJsonObj = new JSONObject();

        if (values == null || values.size() == 0) {
            return resultJsonObj;
        }

        Set<String> keys = values.keySet();
        for (Iterator<String> iterator = keys.iterator(); iterator.hasNext(); ) {

            String key = iterator.next();
            List<String> value = values.get(key);

            try {

                // 当只有一个条目，则直接转化为相应的对象 JsonArray 或者 JsonObject 或者 String
                if (value.size() == 1) {
                    resultJsonObj.put(key, parse2JsonObj(value.get(0)));
                }

                // 多于一个转化为JsonArray
                else {
                    resultJsonObj.put(key, parseListToJson(value));
                }
            } catch (Exception e) {
            }
        }

        return resultJsonObj;
    }

    /**
     * List转化为JsonArray
     *
     * @param list
     * @return
     */
    private static JSONArray parseListToJson(List<String> list) {

        JSONArray jsonArray = new JSONArray();

        if (list == null || list.size() == 0) {
            return jsonArray;
        }

        for (int i = 0; i < list.size(); i++) {

            String value = list.get(i);

            if (TextUtils.isEmpty(value)) {
                continue;
            }

            jsonArray.put(parse2JsonObj(value));
        }

        return jsonArray;
    }

    /**
     * 由于Map中可能存在重命键值，将重合键值放入一个ArrayList中
     *
     * @param values
     * @return
     */
    private static Map<String, ArrayList<String>> transMap(
            Map<String, String> values) {

        if (values == null || values.size() == 0) {
            return null;
        }

        Map<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>>();

        Set<String> keys = values.keySet();
        for (Iterator<String> iterator = keys.iterator(); iterator.hasNext(); ) {

            String key = iterator.next();
            String value = values.get(key);

            value = (TextUtils.isEmpty(value) ? "" : value);

            if (result.keySet().contains(key)) {
                result.get(key).add(value);
            } else {
                ArrayList<String> list = new ArrayList<String>();
                list.add(value);
                result.put(key, list);
            }
        }

        return result;
    }

    /**
     * 将字符串转化为JSON对象，注意如果非有效JSON格式，则直接返回字符串
     *
     * @param value
     * @return
     * @throws JSONException
     */
    public static Object parse2JsonObj(String value) {

        if (TextUtils.isEmpty(value)) {
            return "";
        }

        Object result = value;

        try {

            // 由于Json不区分 [bb]与["bb"]，加这个判断是为了避免[bb]被错误转换为JsonArray
            if (value.indexOf("\"") < 0) {
                return value;
            }

            // 去掉前面的空格方便后面用startsWith
            value = value.trim();
            if (value.startsWith("{") || value.startsWith("[")) {
                result = new JSONTokener(value).nextValue();
            }
        } catch (Exception e) {
        }

        if (result == null) {
            result = value;
        }

        return result;
    }
}
