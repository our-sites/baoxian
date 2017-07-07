package com.bao361.insurance.net;

import android.text.TextUtils;

import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.GZIPInputStream;

public abstract class EncrptResponseHandler extends JsonResponseHandler {


    protected abstract void onSuccess(IRequest request, JSONObject response);


    public abstract void onFailure(final IRequest request, RequestError error);


    @Override
    public final void onFailure(IRequest request, int statusCode, String responseBody, Throwable throwable) {
        RequestError error = new RequestError();
        onFailure(request, error);
    }


    @Override
    public final void onSuccess(IRequest request, int statusCode, JSONObject jsonObj) {

        RequestError error = new RequestError();
        try {
            // // TODO: 16/12/19  处理业务请求

            JSONObject status = jsonObj.getJSONObject("status");
            String status_code = status.getString("status_code");
            if ("0".equals(status_code)) {
                JSONObject result = jsonObj.getJSONObject("result");
                onSuccess(request, result);

            } else {
                //发生业务错误
                error.erro_reason = status.getString("status_reason");
                error.erro_code = status.getString("status_code");
                onFailure(request, error);
            }

        } catch (Exception e) {
            onFailure(request, error);
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
