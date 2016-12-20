package com.common.insurance.request;

import com.common.insurance.net.RequestError;

public interface LoadCallback<T> {

    void onLoadSuccess(T t);

    void onLoadFail(RequestError error);
}