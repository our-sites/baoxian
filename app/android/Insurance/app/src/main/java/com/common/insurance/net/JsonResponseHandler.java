package com.common.insurance.net;

import android.text.TextUtils;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;

public class JsonResponseHandler extends TextReponseHandler {


    public void onSuccess(IRequest request, int statusCode,
                          JSONObject jsonObj) {
    }

    public void onFailure(IRequest request, int statusCode, String responseBody, Throwable error) {
    }


    private void onRequestSuccess(IRequest request, int statusCode, JSONObject jsonObj) {
        onSuccess(request, statusCode, jsonObj);
    }


    private void onRequestFailure(IRequest request, int statusCode, String responseBody, Throwable error) {
        onFailure(request, statusCode, responseBody, error);
    }


    @Override
    public void onFailure(IRequest request, Throwable error) {
        onFailure(request, -1, null, error);
    }

    @Override
    public final void onSuccess(IRequest request, int statusCode, String responseContent) {
        try {

            Object jsonResponse = parse2JsonaObj(responseContent);

            if (jsonResponse == null) {
                onRequestFailure(request, statusCode, (String) jsonResponse,
                        new JSONException(
                                "Response cannot be null"));
            }

            if (jsonResponse instanceof JSONObject) {
                onRequestSuccess(request, statusCode, (JSONObject) jsonResponse);
            } else if (jsonResponse instanceof String) {
                onRequestFailure(request, statusCode, (String) jsonResponse,
                        new JSONException(
                                "Response cannot be parsed as JSON data，data[" + jsonResponse +
                                        "]"));
            } else {
                onRequestFailure(request, statusCode, responseContent,
                        new JSONException("Unexpected response type "
                                + jsonResponse.getClass().getName()));
            }
        } catch (Exception e) {
            onRequestFailure(request, statusCode, responseContent, e);
        } catch (Error error) {
            onRequestFailure(request, statusCode, responseContent, error);
        }

    }


    private Object parse2JsonaObj(String responseBody) throws JSONException {

        if (TextUtils.isEmpty(responseBody)) {
            return null;
        }

        Object result = responseBody;

        // 去掉前面的空格方便后面用startsWith
        responseBody = responseBody.trim();
        if (responseBody.startsWith("{")) {
            result = new JSONTokener(responseBody).nextValue();
        }

        if (result == null) {
            result = responseBody;
        }

        return result;
    }
}
