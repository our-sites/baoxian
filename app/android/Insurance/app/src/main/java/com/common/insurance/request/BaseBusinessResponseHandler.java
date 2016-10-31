package com.common.insurance.request;

import com.common.insurance.net.EncrptResponseHandler;
import com.common.insurance.net.IRequest;

import org.json.JSONArray;
import org.json.JSONObject;


public abstract class BaseBusinessResponseHandler extends EncrptResponseHandler {


    protected abstract void onRequestSuccess(Object jsonObj);


    protected abstract void onRequestFail();


    protected abstract Object parseResponse(Object jsonObj) throws Exception;

    @Override
    public final void onSuccess(IRequest request, JSONObject jsonObj) {

        try {

            Object response = parseResponse(jsonObj);

            if (response != null) {
                onRequestSuccess(response);
            } else {
                sendRequestFail();
            }

        } catch (Exception e) {
            sendRequestFail();
        }
    }

    @Override
    public final void onSuccess(IRequest request, JSONArray jsonArray) {

        try {

            Object response = parseResponse(jsonArray);

            if (response != null) {
                onRequestSuccess(response);
            } else {
                sendRequestFail();
            }

        } catch (Exception e) {
            sendRequestFail();
        }
    }

    @Override
    public final void onFailure(IRequest request) {
        sendRequestFail();
    }

    private void sendRequestFail() {
        onRequestFail();
    }
}
