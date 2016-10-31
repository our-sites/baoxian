package com.common.insurance.net;

import android.text.TextUtils;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.GZIPInputStream;

public class EncrptResponseHandler extends JsonResponseHandler {


    public void onSuccess(IRequest request, JSONObject response) {
    }

    public void onSuccess(IRequest request, JSONArray response) {
    }

    private void onRequestSuccess(final IRequest request, final JSONArray response) {


        onSuccess(request, response);
    }

    private void onRequestSuccess(final IRequest request, final JSONObject response) {

        onSuccess(request, response);
    }

    public void onFailure(final IRequest request) {
    }


    public final void onRequestFailure(final IRequest request, String responseBody) {


        onFailure(request);

    }

    @Override
    public final void onFailure(IRequest request, int statusCode, String responseBody, Throwable error) {


        onRequestFailure(request, responseBody);
    }


    @Override
    public final void onSuccess(IRequest request, int statusCode, JSONArray jsonArray) {

        try {

            JSONObject contentJsonObj = jsonArray.getJSONObject(0);

            // 有code字段即为失败
            if (contentJsonObj.has("code")) {
                int errorCode = contentJsonObj.optInt("code");
                String errorMessage = contentJsonObj.optString("message");
                onRequestFailure(request, jsonArray.toString());
            }

            // 成功
            else {
                onRequestSuccess(request, jsonArray);
            }

        } catch (Exception e) {
            onRequestFailure(request, jsonArray == null ? "" : jsonArray.toString());
        }
    }

    @Override
    public final void onSuccess(IRequest request, int statusCode, JSONObject jsonObj) {

        try {
            onRequestSuccess(request, jsonObj);

        } catch (Exception e) {
            onRequestFailure(request, jsonObj == null ? "" : jsonObj.toString());
        }
    }


    private boolean shouldDecrypt() {

        return true;
    }


    /**
     * GZIP解压缩
     *
     * @param b
     * @return
     */
    private static byte[] uncompressData(byte[] b) {

        if (b == null || b.length == 0) {
            return null;
        }

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayInputStream in = new ByteArrayInputStream(b);
        GZIPInputStream gUnzip = null;

        try {
            gUnzip = new GZIPInputStream(in);
            byte[] buffer = new byte[256];
            int n;

            while ((n = gUnzip.read(buffer)) >= 0) {
                out.write(buffer, 0, n);
            }

            return out.toByteArray();
        } catch (IOException e) {
        } finally {
            try {
                if (out != null) {
                    out.close();
                }
                if (gUnzip != null) {
                    gUnzip.close();
                }
            } catch (Exception e2) {
            }
        }

        return null;
    }


    /**
     * 把URL参数转换为key value的形式
     */
    private static Map<String, String> paseUrlParamsToKeyValue(String urlParams) {

        if (TextUtils.isEmpty(urlParams)) {
            return new HashMap<String, String>();
        }

        String dataPart = urlParams.replaceAll("amp;", "");

        String[] keyvalues = dataPart.split("&");

        Map<String, String> map = new HashMap<String, String>();
        for (int i = 0; i < keyvalues.length; i++) {
            String[] keyvalue = keyvalues[i].split("=");
            if (keyvalue.length > 1) {
                map.put(keyvalue[0], keyvalue[1]);
            }
        }

        return map;
    }


}
