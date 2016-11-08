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

    public void onFailure(final IRequest request) {
    }


    private void onRequestSuccess(final IRequest request, final JSONArray response) {


        onSuccess(request, response);
    }

    private void onRequestSuccess(final IRequest request, final JSONObject response) {

        onSuccess(request, response);
    }


    public final void onRequestFailure(final IRequest request, String responseBody) {


        onFailure(request);

    }

    @Override
    public final void onFailure(IRequest request, int statusCode, String responseBody, Throwable error) {

        onRequestFailure(request, responseBody);
    }


    @Override
    public final void onSuccess(IRequest request, int statusCode, JSONObject jsonObj) {

        try {
            //// TODO: 16/10/28 处理业务相应信息

            onRequestSuccess(request, jsonObj);

        } catch (Exception e) {
            onRequestFailure(request, jsonObj == null ? "" : jsonObj.toString());
        }
    }


    @Override
    public byte[] prepareResponseData(IRequest request, byte[] responseData) throws Exception {
        //解密，解压缩
        return super.prepareResponseData(request, responseData);
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
