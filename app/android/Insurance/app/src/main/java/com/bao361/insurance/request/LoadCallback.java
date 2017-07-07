package com.bao361.insurance.request;

import com.bao361.insurance.net.RequestError;

public interface LoadCallback<T> {

    void onLoadSuccess(T t);

    void onLoadFail(RequestError error);
}