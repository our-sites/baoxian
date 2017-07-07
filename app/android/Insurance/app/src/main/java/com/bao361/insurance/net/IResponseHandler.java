package com.bao361.insurance.net;


import java.io.InputStream;

public interface IResponseHandler<T> {

    void onStart();

    void onFinish();

    void onProgress(long progress);

    void onSuccess(IRequest request, int statusCode, T responseBytes);

    void onFailure(IRequest request, Throwable error);

    void onRetry();

    T parseResponse(IRequest request, InputStream inputStream, long contentLength) throws Exception;
}
