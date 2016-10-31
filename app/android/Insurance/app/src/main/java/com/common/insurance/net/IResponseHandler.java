package com.common.insurance.net;


import java.io.InputStream;

public abstract class IResponseHandler<T> {


    public void onStart() {
    }


    public void onFinish() {
    }


    public abstract void onCancel();


    public void publishProgress(final int progress) {
    }


    protected void onProgress(int progress) {
    }


    public abstract void onSuccess(IRequest request, int statusCode, T responseBytes);


    public abstract void onFailure(IRequest request, int statusCode, T responseBody, Throwable error);


    public abstract void onFailure(IRequest request, Throwable error);

    public void onRetry() {
    }


    public abstract T parseResponse(IRequest request, InputStream inputStream,
                                    long contentLength) throws Exception;
}
