package com.common.insurance.net;

import java.io.UnsupportedEncodingException;


public abstract class TextReponseHandler extends DefaultResponseHandler {

    protected static final String DEFAULT_CHARSET = "UTF-8";

    private String mCharset;

    public TextReponseHandler() {
        this(DEFAULT_CHARSET);
    }

    public TextReponseHandler(String charset) {
        this.mCharset = charset;
    }

    public String getCharset() {
        return mCharset;
    }


    public abstract void onSuccess(IRequest request, int statusCode, String responseContent);


    public void onFailure(IRequest request, int statusCode, String responseBody, Throwable error) {
    }

    @Override
    public final void onSuccess(IRequest request, int statusCode, byte[] responseBytes) {
        onSuccess(request, statusCode, getResponseString(responseBytes, mCharset));
    }

    @Override
    public final void onFailure(IRequest request, int statusCode, byte[] responseBytes, Throwable error) {


        onFailure(request, statusCode, getResponseString(responseBytes, mCharset), error);
    }


    private String getResponseString(byte[] stringBytes, String charset) {

        try {
            return stringBytes == null ? null
                    : new String(stringBytes, charset);
        } catch (UnsupportedEncodingException e) {
        }
        return null;
    }
}
