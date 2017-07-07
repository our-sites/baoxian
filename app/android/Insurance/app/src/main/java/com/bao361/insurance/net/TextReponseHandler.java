package com.bao361.insurance.net;

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


    @Override
    public final void onSuccess(IRequest request, int statusCode, byte[] responseBytes) {
        onSuccess(request, statusCode, getResponseString(responseBytes, mCharset));
    }

    @Override
    public void onFailure(IRequest request, Throwable error) {
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
